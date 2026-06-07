import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
import requests
import pandas as pd
import difflib
import pytesseract
from PIL import Image
from clinical.prescription_parser import PrescriptionParser
from utils.pdf_generator import generate_pdf

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

API_URL = "http://127.0.0.1:8000"

parser = PrescriptionParser("data/raw/drug_metadata.csv")

drug_df = pd.read_csv("data/raw/drug_metadata.csv")
drug_list_master = sorted(drug_df["drug_name"].dropna().unique().tolist())


# ------------------------------
# Risk Level
# ------------------------------
def risk_level(score):
    if score < 150:
        return "🟢 Low Risk"
    elif score < 350:
        return "🟡 Moderate Risk"
    else:
        return "🔴 High Risk"


# ------------------------------
# Risk Bar
# ------------------------------
def build_risk_bar(score, max_score=600):
    try:
        score = float(score)
    except:
        return "No risk data"

    percent = min(score / max_score, 1.0)
    filled = int(percent * 20)
    empty = 20 - filled

    bar = "█" * filled + "░" * empty
    return f"[{bar}] {int(score)} / {max_score}"


# ------------------------------
# Timeline
# ------------------------------
def build_timeline(schedule_text):

    lines = schedule_text.split("\n")
    timeline = ["Daily Medication Timeline", "---------------------------------"]

    for line in lines:
        if "AM -" in line or "PM -" in line:
            parts = line.split("-")
            time = parts[0].strip()
            drug = parts[1].strip()
            timeline.append(f"{time} | {drug}")

    timeline.append("---------------------------------")
    return "\n".join(timeline)


# ------------------------------
# Parse Input
# ------------------------------
def parse_input(dropdown_drugs, text_input):

    if dropdown_drugs:
        return dropdown_drugs

    if text_input:
        if "," in text_input:
            return [d.strip() for d in text_input.split(",") if d.strip()]
        return parser.extract_drugs(text_input)

    return []


# ------------------------------
# Smart Validation
# ------------------------------
def validate_and_suggest(drugs):

    known = []
    unknown = []
    suggestions = {}

    master_lower = [d.lower() for d in drug_list_master]

    for d in drugs:
        d_lower = d.lower()

        if d_lower in master_lower:
            known.append(d)
        else:
            matches = difflib.get_close_matches(d_lower, master_lower, n=1, cutoff=0.75)

            if matches:
                matched = matches[0]
                suggestions[d] = matched
                known.append(matched)
            else:
                unknown.append(d)

    return known, unknown, suggestions


# ------------------------------
# PDF Download
# ------------------------------
def download_report(risk, category, breakdown, interactions,
                    food, alternatives, schedule, lab, explanation):

    data = {
        "risk_score": risk,
        "risk_category": category,
        "breakdown": breakdown,
        "interactions": interactions,
        "food": food,
        "alternatives": alternatives,
        "schedule": schedule,
        "lab": lab,
        "explanation": explanation
    }

    return generate_pdf(data)


# ------------------------------
# Analyze
# ------------------------------
def analyze(dropdown_drugs, text_input, age, sex, weight,
            kidney_disease, liver_disease,
            smoker, alcohol,
            conditions, allergies,
            creatinine, alt, ast):

    drug_list = parse_input(dropdown_drugs, text_input)

    known, unknown, suggestions = validate_and_suggest(drug_list)

    if not known:
        return (0, "❌ No valid drugs", "", "All drugs unknown",
                "", "", "", "", "", "⚠️ Check drug names")

    # Unknown + suggestions message
    unknown_text = ""

    if unknown:
        unknown_text += "⚠️ Unknown drugs:\n"
        for u in unknown:
            unknown_text += f"- {u}\n"

    if suggestions:
        unknown_text += "\n🔍 Suggested corrections:\n"
        for k, v in suggestions.items():
            unknown_text += f"- {k} → {v}\n"

    # API call
    response = requests.post(
        f"{API_URL}/analyze",
        json={
            "drugs": known,
            "age": int(age),
            "sex": sex,
            "weight": weight,
            "kidney_disease": kidney_disease,
            "liver_disease": liver_disease,
            "smoker": smoker,
            "alcohol_use": alcohol,
            "conditions": [c.strip() for c in conditions.split(",") if c],
            "allergies": [a.strip() for a in allergies.split(",") if a],
            "creatinine": creatinine,
            "alt": alt,
            "ast": ast
        }
    )

    result = response.json()

    timeline = build_timeline(result["schedule"])

    risk_score = result["risk_analysis"]["final_risk_score"]
    risk_category = risk_level(risk_score)
    risk_bar = build_risk_bar(risk_score)

    rb = result["risk_analysis"].get("risk_breakdown", {})

    breakdown_text = (
        f"Toxicity: {rb.get('toxicity_component', 0)}\n"
        f"Comorbidity: {rb.get('comorbidity_penalty', 0)}\n"
        f"Lifestyle: {rb.get('lifestyle_penalty', 0)}\n"
        f"Liver Penalty: {rb.get('liver_penalty', 0)}\n"
        f"Interactions: {rb.get('interaction_penalty', 0)}\n"
        f"Food: {rb.get('food_penalty', 0)}\n"
        f"Kidney Multiplier: {rb.get('kidney_multiplier', 1.0)}\n"
        f"Liver Multiplier: {rb.get('liver_multiplier', 1.0)}\n"
        f"Total: {rb.get('total', 0)}"
    )

    lab = result["risk_analysis"].get("lab_analysis", {})

    lab_text = (
        f"eGFR: {lab.get('egfr', 'N/A')}\n"
        f"Kidney Multiplier: {lab.get('kidney_multiplier', 'N/A')}\n"
        f"ALT: {lab.get('alt', 'N/A')}\n"
        f"AST: {lab.get('ast', 'N/A')}\n"
        f"Liver Multiplier: {lab.get('liver_multiplier', 'N/A')}"
    )

    explanations = result["risk_analysis"].get("explanations", [])

    explanation_text = ""
    if unknown_text:
        explanation_text += unknown_text + "\n\n"

    explanation_text += "\n".join(explanations) if explanations else "No major risk factors detected"

    interaction_text = "\n\n".join(
        [f"{i['drug_pair']} → {i['interaction_type']}"
         for i in result["risk_analysis"]["interactions"]]
    ) or "No interactions"

    food_text = "\n\n".join(
        [f"{f['drug']} + {f['food']}"
         for f in result["risk_analysis"].get("food_interactions", [])]
    ) or "No food interactions"

    alt_text = "\n".join(
        [f"{a['drug']} → {', '.join(a['alternatives'])}"
         for a in result["risk_analysis"].get("alternatives", [])]
    ) or "No alternatives"

    return (
        risk_score,
        risk_category,
        risk_bar,
        breakdown_text,
        interaction_text,
        food_text,
        alt_text,
        timeline,
        lab_text,
        explanation_text
    )


# ------------------------------
# UI (FINAL PRODUCT)
# ------------------------------
with gr.Blocks() as app:

    gr.Markdown("# 🧠 MediWise — Clinical Intelligence System")
    gr.Markdown("👉 Enter patient details and analyze medication risk")

    with gr.Row():

        # LEFT PANEL
        with gr.Column(scale=1):

            gr.Markdown("## 📝 Inputs")

            drug_dropdown = gr.Dropdown(choices=drug_list_master, multiselect=True)
            drug_text = gr.Textbox(label="Or enter drugs")

            age = gr.Number(label="Age", value=30)
            sex = gr.Dropdown(["male", "female"], value="male")
            weight = gr.Number(label="Weight")

            creatinine = gr.Number(label="Creatinine")
            alt = gr.Number(label="ALT")
            ast = gr.Number(label="AST")

            kidney = gr.Checkbox(label="Kidney Disease")
            liver = gr.Checkbox(label="Liver Disease")

            smoker = gr.Checkbox(label="Smoker")
            alcohol = gr.Checkbox(label="Alcohol")

            conditions = gr.Textbox(label="Conditions")
            allergies = gr.Textbox(label="Allergies")

            analyze_btn = gr.Button("🚀 Analyze")

        # RIGHT PANEL
        with gr.Column(scale=2):

            gr.Markdown("## 📊 Results")

            risk_output = gr.Number(label="Risk Score")
            risk_category_output = gr.Textbox(label="Risk Category")
            risk_bar_output = gr.Textbox(label="Risk Meter")

            breakdown_output = gr.Textbox(label="Breakdown")

            with gr.Accordion("🧪 Lab", open=False):
                lab_output = gr.Textbox()

            with gr.Accordion("⚠️ Interactions", open=False):
                interaction_output = gr.Textbox()

            with gr.Accordion("🍽 Food", open=False):
                food_output = gr.Textbox()

            with gr.Accordion("💡 Alternatives", open=False):
                alternative_output = gr.Textbox()

            with gr.Accordion("🕒 Schedule", open=False):
                schedule_output = gr.Textbox()

            with gr.Accordion("🧠 Explanation", open=True):
                explanation_output = gr.Textbox(lines=12)

            download_btn = gr.Button("📄 Download Report")
            file_output = gr.File()

    analyze_btn.click(
        analyze,
        inputs=[
            drug_dropdown, drug_text,
            age, sex, weight,
            kidney, liver,
            smoker, alcohol,
            conditions, allergies,
            creatinine, alt, ast
        ],
        outputs=[
            risk_output,
            risk_category_output,
            risk_bar_output,
            breakdown_output,
            interaction_output,
            food_output,
            alternative_output,
            schedule_output,
            lab_output,
            explanation_output
        ]
    )

    download_btn.click(
        download_report,
        inputs=[
            risk_output,
            risk_category_output,
            breakdown_output,
            interaction_output,
            food_output,
            alternative_output,
            schedule_output,
            lab_output,
            explanation_output
        ],
        outputs=file_output
    )

app.launch()