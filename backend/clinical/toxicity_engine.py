import pandas as pd


class ToxicityEngine:

    def __init__(self, metadata_path):
        self.drug_data = pd.read_csv(metadata_path)
        self.drug_data["drug_name"] = self.drug_data["drug_name"].str.lower()

    def get_drug_info(self, drug_name):

        drug_name = drug_name.lower()

        drug = self.drug_data[self.drug_data["drug_name"] == drug_name]

        if drug.empty:
            raise ValueError(f"Drug {drug_name} not found in dataset")

        return drug.iloc[0]

    def compute_toxicity_score(
        self,
        drug_name,
        age,
        liver_disease=False,
        kidney_disease=False
    ):

        drug = self.get_drug_info(drug_name)

        base_score = (
            15 * drug["hepatic_risk_level"]
            + 15 * drug["renal_risk_level"]
            + 20 * drug["black_box_warning"]
            + 10 * drug["narrow_therapeutic_index"]
        )

        multiplier = 1

        if age > 65:
            multiplier += 0.5

        if liver_disease:
            multiplier += 0.5

        if kidney_disease:
            multiplier += 0.5

        final_score = base_score * multiplier

        return float(round(final_score, 2))

    def risk_tier(self, score):

        if score <= 20:
            return "Low"

        elif score <= 50:
            return "Moderate"

        else:
            return "High"