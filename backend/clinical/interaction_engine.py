import pandas as pd
from graph.predict_interaction import GNNInteractionPredictor


class InteractionEngine:

    def __init__(self, interaction_path):

        self.interactions = pd.read_csv(interaction_path)

        self.interactions["drug_a"] = self.interactions["drug_a"].str.lower()
        self.interactions["drug_b"] = self.interactions["drug_b"].str.lower()

        # Initialize GNN predictor
        self.gnn_predictor = GNNInteractionPredictor(
            model_path="graph/models/gnn_edge_predictor.pt",
            interaction_path=interaction_path
        )

    def check_interaction(self, drug1, drug2):

        drug1 = drug1.lower()
        drug2 = drug2.lower()

        # -----------------------------
        # 1. Rule-based known interaction
        # -----------------------------
        result = self.interactions[
            ((self.interactions["drug_a"] == drug1) & (self.interactions["drug_b"] == drug2)) |
            ((self.interactions["drug_a"] == drug2) & (self.interactions["drug_b"] == drug1))
        ]

        if not result.empty:
            row = result.iloc[0]

            return {
                "drug_pair": f"{drug1.capitalize()} + {drug2.capitalize()}",
                "interaction_type": row["interaction_type"],
                "severity_level": int(row["severity_level"]),
                "mechanism": row["mechanism"],
                "recommended_spacing_hours": int(row["recommended_spacing_hours"]),
                "source": "Known Database"
            }

        # -----------------------------
        # 2. GNN-predicted interaction
        # -----------------------------
        prediction = self.gnn_predictor.predict(drug1, drug2)

        if prediction["interaction_probability"] is not None and prediction["predicted_interaction"]:

            probability = prediction["interaction_probability"]

            # Convert probability to severity level
            if probability >= 0.85:
                severity = 4
            elif probability >= 0.70:
                severity = 3
            else:
                severity = 2

            return {
                "drug_pair": f"{drug1.capitalize()} + {drug2.capitalize()}",
                "interaction_type": "predicted_interaction",
                "severity_level": severity,
                "mechanism": f"AI-predicted interaction likelihood ({probability}) based on graph relationships",
                "recommended_spacing_hours": 0,
                "source": "GNN Prediction"
            }

        return None

    def check_all_interactions(self, drugs):

        found_interactions = []

        for i in range(len(drugs)):
            for j in range(i + 1, len(drugs)):

                interaction = self.check_interaction(drugs[i], drugs[j])

                if interaction:
                    found_interactions.append(interaction)

        return found_interactions