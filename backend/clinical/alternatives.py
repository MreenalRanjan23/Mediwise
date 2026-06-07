import pandas as pd
from clinical.similarity_engine import SimilarityEngine


class AlternativeEngine:

    def __init__(self, metadata_path, interaction_engine=None):

        self.sim_engine = SimilarityEngine(metadata_path)
        self.df = pd.read_csv(metadata_path)
        self.interaction_engine = interaction_engine

    # -----------------------------
    # Get drug class
    # -----------------------------
    def get_drug_class(self, drug):

        row = self.df[self.df["drug_name"].str.lower() == drug.lower()]

        if row.empty:
            return None

        return row.iloc[0].get("drug_class", None)

    # -----------------------------
    # Get patient-aware alternatives 🔥
    # -----------------------------
    def suggest(self, drugs, patient_profile):

        suggestions = []

        for drug in drugs:

            drug_class = self.get_drug_class(drug)
            similar = self.sim_engine.get_similar_drugs(drug, top_n=10)

            filtered = []

            for name, score in similar:

                # -----------------------------
                # 1. Same class filter
                # -----------------------------
                if drug_class:
                    if self.get_drug_class(name) != drug_class:
                        continue

                # -----------------------------
                # 2. Interaction filter
                # -----------------------------
                if self.interaction_engine:
                    interactions = self.interaction_engine.check_all_interactions([drug, name])
                    if interactions:
                        continue

                # -----------------------------
                # 3. Patient safety filter 🔥
                # -----------------------------
                row = self.df[self.df["drug_name"].str.lower() == name.lower()]

                if not row.empty:

                    hepatic_risk = row.iloc[0].get("hepatic_risk_level", 0)
                    renal_risk = row.iloc[0].get("renal_risk_level", 0)

                    # Liver disease
                    if patient_profile.liver_disease and hepatic_risk >= 3:
                        continue

                    # Kidney disease
                    if patient_profile.kidney_disease and renal_risk >= 3:
                        continue

                filtered.append((name, score))

                if len(filtered) >= 3:
                    break

            formatted = [
                f"{n} (score: {round(s, 2)})"
                for n, s in filtered
            ]

            suggestions.append({
                "drug": drug,
                "alternatives": formatted if formatted else ["No safe alternatives found"]
            })

        return suggestions