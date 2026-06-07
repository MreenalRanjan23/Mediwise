import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clinical.interaction_engine import InteractionEngine

engine = InteractionEngine("data/raw/drug_interactions.csv")

drugs = ["warfarin", "ibuprofen", "paracetamol"]

results = engine.check_all_interactions(drugs)

print("\n=== INTERACTION RESULTS ===\n")

for r in results:
    print(r)