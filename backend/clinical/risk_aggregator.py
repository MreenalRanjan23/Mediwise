from clinical.toxicity_engine import ToxicityEngine
from clinical.interaction_engine import InteractionEngine
from clinical.food_interaction_engine import FoodInteractionEngine
from clinical.alternatives import AlternativeEngine
from clinical.lab_engine import (
    calculate_egfr,
    kidney_risk_multiplier,
    liver_risk_multiplier
)
from clinical.comorbidity_engine import ComorbidityEngine
from clinical.lifestyle_engine import LifestyleEngine
from clinical.explainability_engine import ExplainabilityEngine  # 🔥 NEW


class RiskAggregator:

    def __init__(self, metadata_path, interaction_path):

        self.toxicity_engine = ToxicityEngine(metadata_path)
        self.interaction_engine = InteractionEngine(interaction_path)
        self.food_engine = FoodInteractionEngine("data/raw/food_interactions.csv")

        self.alternative_engine = AlternativeEngine(
            metadata_path,
            self.interaction_engine
        )

        self.comorbidity_engine = ComorbidityEngine(metadata_path)
        self.lifestyle_engine = LifestyleEngine()

        # 🔥 NEW
        self.explain_engine = ExplainabilityEngine()

    def analyze_medication_plan(self, drugs, patient_profile):

        toxicity_results = []
        total_score = 0
        total_comorbidity_penalty = 0
        total_lifestyle_penalty = 0
        total_liver_penalty = 0

        multiplier = patient_profile.get_risk_multiplier()

        # -----------------------------
        # 1. Drug-level scoring
        # -----------------------------
        for drug in drugs:

            base_score = self.toxicity_engine.compute_toxicity_score(
                drug,
                patient_profile.age,
                patient_profile.liver_disease,
                patient_profile.kidney_disease
            )

            adjusted_score = base_score * multiplier

            # -----------------------------
            # Comorbidity
            # -----------------------------
            comorbidity_penalty, comorbidity_reasons = self.comorbidity_engine.get_penalty(
                drug,
                patient_profile.conditions
            )

            adjusted_score += comorbidity_penalty
            total_comorbidity_penalty += comorbidity_penalty

            # -----------------------------
            # Lifestyle
            # -----------------------------
            lifestyle_penalty, lifestyle_reasons = self.lifestyle_engine.get_penalty(
                drug,
                patient_profile
            )

            adjusted_score += lifestyle_penalty
            total_lifestyle_penalty += lifestyle_penalty

            # -----------------------------
            # Liver-specific penalty
            # -----------------------------
            liver_penalty = 0
            liver_reasons = []

            if patient_profile.alt and patient_profile.alt > 60:
                if drug.lower() in ["paracetamol", "acetaminophen"]:
                    liver_penalty += 30
                    liver_reasons.append("Elevated ALT + hepatotoxic drug")

            adjusted_score += liver_penalty
            total_liver_penalty += liver_penalty

            toxicity_results.append({
                "drug": drug,
                "base_score": float(base_score),
                "adjusted_score": float(adjusted_score),
                "risk_tier": self.toxicity_engine.risk_tier(adjusted_score),

                "comorbidity_penalty": float(comorbidity_penalty),
                "comorbidity_reasons": comorbidity_reasons,

                "lifestyle_penalty": float(lifestyle_penalty),
                "lifestyle_reasons": lifestyle_reasons,

                "liver_penalty": float(liver_penalty),
                "liver_reasons": liver_reasons
            })

            total_score += adjusted_score

        # -----------------------------
        # 2. Interactions
        # -----------------------------
        interactions = self.interaction_engine.check_all_interactions(drugs)
        interaction_penalty = sum(i["severity_level"] * 5 for i in interactions)

        # -----------------------------
        # 3. Food
        # -----------------------------
        food_interactions = self.food_engine.check_food_interactions(drugs)

        food_penalty = 0
        for f in food_interactions:
            if f["interaction_type"] == "absorption_reduction":
                food_penalty += 10
            elif f["interaction_type"] == "effect_reduction":
                food_penalty += 15
            elif f["interaction_type"] == "toxicity_increase":
                food_penalty += 25
            elif f["interaction_type"] == "severe_reaction":
                food_penalty += 40

        # -----------------------------
        # 4. Lab Intelligence
        # -----------------------------
        egfr = calculate_egfr(
            patient_profile.creatinine,
            patient_profile.age,
            patient_profile.sex
        )

        kidney_multiplier = kidney_risk_multiplier(egfr)

        liver_multiplier = liver_risk_multiplier(
            patient_profile.alt,
            patient_profile.ast
        )

        combined_multiplier = kidney_multiplier * liver_multiplier

        # -----------------------------
        # 5. Alternatives
        # -----------------------------
        alternatives = self.alternative_engine.suggest(drugs, patient_profile)

        # -----------------------------
        # 6. Final Score
        # -----------------------------
        base_score = total_score + interaction_penalty + food_penalty
        final_score = float(base_score * combined_multiplier)

        # -----------------------------
        # 7. Breakdown
        # -----------------------------
        risk_breakdown = {
            "toxicity_component": float(total_score),
            "comorbidity_penalty": float(total_comorbidity_penalty),
            "lifestyle_penalty": float(total_lifestyle_penalty),
            "liver_penalty": float(total_liver_penalty),
            "interaction_penalty": float(interaction_penalty),
            "food_penalty": float(food_penalty),
            "kidney_multiplier": float(kidney_multiplier),
            "liver_multiplier": float(liver_multiplier),
            "total": float(final_score)
        }

        # -----------------------------
        # 8. Lab Analysis
        # -----------------------------
        lab_analysis = {
            "egfr": egfr,
            "kidney_multiplier": kidney_multiplier,
            "alt": patient_profile.alt,
            "ast": patient_profile.ast,
            "liver_multiplier": liver_multiplier
        }

        # -----------------------------
        # 🔥 9. Explainability
        # -----------------------------
        explanations = self.explain_engine.generate({
            "toxicity_results": toxicity_results,
            "interactions": interactions,
            "lab_analysis": lab_analysis
        })

        return {
            "toxicity_results": toxicity_results,
            "interactions": interactions,
            "food_interactions": food_interactions,
            "alternatives": alternatives,
            "final_risk_score": final_score,
            "risk_breakdown": risk_breakdown,
            "lab_analysis": lab_analysis,
            "explanations": explanations,   # 🔥 NEW
            "patient_profile": patient_profile.summary()
        }