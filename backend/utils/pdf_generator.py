from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, filename="report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    elements = []

    def add(title, content):
        elements.append(Paragraph(f"<b>{title}</b>", styles["Heading3"]))
        elements.append(Spacer(1, 8))
        elements.append(Paragraph(content.replace("\n", "<br/>"), styles["Normal"]))
        elements.append(Spacer(1, 15))

    add("Risk Score", f"{data['risk_score']} ({data['risk_category']})")
    add("Breakdown", data["breakdown"])
    add("Lab Analysis", data["lab"])
    add("Interactions", data["interactions"])
    add("Food Interactions", data["food"])
    add("Alternatives", data["alternatives"])
    add("Schedule", data["schedule"])
    add("Explanation", data["explanation"])

    doc.build(elements)

    return filename