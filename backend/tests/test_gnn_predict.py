import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph.predict_interaction import GNNInteractionPredictor

predictor = GNNInteractionPredictor(
    model_path="graph/models/gnn_edge_predictor.pt",
    interaction_path="data/raw/drug_interactions.csv"
)

print("\n=== TEST 1 ===")
print(predictor.predict("warfarin", "ibuprofen"))

print("\n=== TEST 2 ===")
print(predictor.predict("warfarin", "paracetamol"))

print("\n=== TEST 3 ===")
print(predictor.predict("ciprofloxacin", "calcium"))