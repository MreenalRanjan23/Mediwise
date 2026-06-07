class ComorbidityEngine:

    def __init__(self, metadata_path):
        import pandas as pd
        self.df = pd.read_csv(metadata_path)

    def get_drug_class(self, drug):
        row = self.df[self.df["drug_name"].str.lower() == drug.lower()]
        if row.empty:
            return None
        return row.iloc[0].get("drug_class", None)

    def get_penalty(self, drug, conditions):

        drug_class = self.get_drug_class(drug)
        if not drug_class:
            return 0, []

        penalty = 0
        reasons = []

        conditions = [c.lower() for c in conditions]

        # -----------------------------
        # Hypertension
        # -----------------------------
        if "hypertension" in conditions and drug_class == "NSAID":
            penalty += 30
            reasons.append("NSAIDs may increase blood pressure")

        # -----------------------------
        # GI Ulcer
        # -----------------------------
        if "ulcer" in conditions and drug_class == "NSAID":
            penalty += 40
            reasons.append("NSAIDs increase risk of GI bleeding")

        # -----------------------------
        # Heart Disease
        # -----------------------------
        if "heart disease" in conditions and drug_class == "NSAID":
            penalty += 35
            reasons.append("NSAIDs increase cardiovascular risk")

        # -----------------------------
        # Diabetes (example rule)
        # -----------------------------
        if "diabetes" in conditions and drug_class == "Steroid":
            penalty += 25
            reasons.append("Steroids elevate blood glucose")

        return penalty, reasons