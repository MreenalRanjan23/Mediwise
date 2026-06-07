import pandas as pd


class FoodInteractionEngine:

    def __init__(self, dataset_path):

        self.food_data = pd.read_csv(dataset_path)

        self.food_data["drug_name"] = self.food_data["drug_name"].str.lower()

    def check_food_interactions(self, drugs):

        results = []

        for drug in drugs:

            drug_lower = drug.lower()

            matches = self.food_data[
                self.food_data["drug_name"] == drug_lower
            ]

            for _, row in matches.iterrows():

                results.append({
                    "drug": drug,
                    "food": row["food"],
                    "interaction_type": row["interaction_type"],
                    "recommendation": row["recommendation"]
                })

        return results