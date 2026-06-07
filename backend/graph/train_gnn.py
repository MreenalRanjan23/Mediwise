import os
import sys
import random
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph.graph_builder import DrugGraphBuilder
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


def build_training_data(interaction_path):
    df = pd.read_csv(interaction_path)

    df["drug_a"] = df["drug_a"].str.lower()
    df["drug_b"] = df["drug_b"].str.lower()

    drugs = sorted(set(df["drug_a"]).union(set(df["drug_b"])))
    drug_to_idx = {drug: i for i, drug in enumerate(drugs)}

    positive_pairs = set()
    for _, row in df.iterrows():
        a = drug_to_idx[row["drug_a"]]
        b = drug_to_idx[row["drug_b"]]
        positive_pairs.add(tuple(sorted((a, b))))

    positive_pairs = list(positive_pairs)

    negative_pairs = set()
    while len(negative_pairs) < len(positive_pairs):
        a, b = random.sample(range(len(drugs)), 2)
        pair = tuple(sorted((a, b)))
        if pair not in positive_pairs:
            negative_pairs.add(pair)

    negative_pairs = list(negative_pairs)

    all_pairs = positive_pairs + negative_pairs
    labels = [1] * len(positive_pairs) + [0] * len(negative_pairs)

    return drugs, drug_to_idx, positive_pairs, all_pairs, labels


def build_graph_edges(positive_pairs):
    edges = []
    for a, b in positive_pairs:
        edges.append([a, b])
        edges.append([b, a])
    return torch.tensor(edges, dtype=torch.long).t().contiguous()


def train_model():
    interaction_path = "data/raw/drug_interactions.csv"

    drugs, drug_to_idx, positive_pairs, all_pairs, labels = build_training_data(interaction_path)

    num_nodes = len(drugs)
    x = torch.eye(num_nodes)
    edge_index = build_graph_edges(positive_pairs)

    base_gnn = DrugInteractionGNN(num_nodes)
    model = EdgePredictor(base_gnn)

    pair_tensor = torch.tensor(all_pairs, dtype=torch.long)
    label_tensor = torch.tensor(labels, dtype=torch.float32)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(100):
        model.train()
        optimizer.zero_grad()

        logits = model(x, edge_index, pair_tensor)
        loss = criterion(logits, label_tensor)

        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            probs = torch.sigmoid(logits)
            preds = (probs > 0.5).float()
            acc = (preds == label_tensor).float().mean().item()

            print(f"Epoch {epoch:03d} | Loss: {loss.item():.4f} | Accuracy: {acc:.4f}")

    os.makedirs("graph/models", exist_ok=True)
    torch.save({
        "model_state_dict": model.state_dict(),
        "drugs": drugs
    }, "graph/models/gnn_edge_predictor.pt")

    print("\nModel saved to: graph/models/gnn_edge_predictor.pt")


if __name__ == "__main__":
    train_model()