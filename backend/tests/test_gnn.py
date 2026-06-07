import sys
import os
import torch

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph.graph_builder import DrugGraphBuilder
from graph.gnn_model import DrugInteractionGNN

# Build graph
builder = DrugGraphBuilder("data/raw/drug_interactions.csv")
G = builder.build_graph()

# Map drugs to indices
nodes = list(G.nodes)
node_to_idx = {node: i for i, node in enumerate(nodes)}

# Create edge_index
edges = []

for u, v in G.edges:
    edges.append([node_to_idx[u], node_to_idx[v]])
    edges.append([node_to_idx[v], node_to_idx[u]])

edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

# Node features (identity matrix)
num_nodes = len(nodes)
x = torch.eye(num_nodes)

# Model
model = DrugInteractionGNN(num_nodes)

# Forward pass
output = model(x, edge_index)

print("Number of nodes:", num_nodes)
print("Edge index shape:", edge_index.shape)
print("Model Output Shape:", output.shape)