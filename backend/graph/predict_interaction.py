import os
import sys
import torch
import torch.nn as nn
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph.gnn_model import DrugInteractionGNN


class EdgePredictor(nn.Module):
    def __init__(self, gnn):
        super().__init__()
        self.gnn = gnn
        self.edge_mlp = nn.Sequential(
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )

    def forward(self, x, edge_index, pair_indices):
        node_embeddings = self.gnn.get_embeddings(x, edge_index)

        src = node_embeddings[pair_indices[:, 0]]
        dst = node_embeddings[pair_indices[:, 1]]

        edge_features = torch.cat([src, dst], dim=1)
        logits = self.edge_mlp(edge_features)

        return logits.squeeze()


class GNNInteractionPredictor:
    def __init__(self, model_path, interaction_path):
        self.model_path = model_path
        self.interaction_path = interaction_path

        # Load saved model data
        checkpoint = torch.load(model_path)

        self.drugs = checkpoint["drugs"]
        self.drug_to_idx = {drug: i for i, drug in enumerate(self.drugs)}

        self.num_nodes = len(self.drugs)
        self.x = torch.eye(self.num_nodes)

        self.edge_index = self.build_graph_edges()

        base_gnn = DrugInteractionGNN(self.num_nodes)
        self.model = EdgePredictor(base_gnn)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()

    def build_graph_edges(self):
        df = pd.read_csv(self.interaction_path)

        df["drug_a"] = df["drug_a"].str.lower()
        df["drug_b"] = df["drug_b"].str.lower()

        edges = []

        for _, row in df.iterrows():
            a = row["drug_a"]
            b = row["drug_b"]

            if a in self.drug_to_idx and b in self.drug_to_idx:
                a_idx = self.drug_to_idx[a]
                b_idx = self.drug_to_idx[b]

                edges.append([a_idx, b_idx])
                edges.append([b_idx, a_idx])

        return torch.tensor(edges, dtype=torch.long).t().contiguous()

    def predict(self, drug_a, drug_b):
        drug_a = drug_a.lower()
        drug_b = drug_b.lower()

        if drug_a not in self.drug_to_idx or drug_b not in self.drug_to_idx:
            return {
                "drug_a": drug_a,
                "drug_b": drug_b,
                "interaction_probability": None,
                "predicted_interaction": None,
                "message": "One or both drugs not present in GNN training graph."
            }

        pair_tensor = torch.tensor(
            [[self.drug_to_idx[drug_a], self.drug_to_idx[drug_b]]],
            dtype=torch.long
        )

        with torch.no_grad():
            logit = self.model(self.x, self.edge_index, pair_tensor)
            probability = torch.sigmoid(logit).item()

        return {
            "drug_a": drug_a,
            "drug_b": drug_b,
            "interaction_probability": round(probability, 4),
            "predicted_interaction": probability > 0.5
        }