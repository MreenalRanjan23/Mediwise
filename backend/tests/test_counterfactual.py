import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clinical.counterfactual_engine import CounterfactualEngine


engine = CounterfactualEngine(
    "data/raw/drug_metadata.csv",
    "data/raw/drug_interactions.csv"
)

drugs = ["Warfarin", "Ibuprofen", "Paracetamol"]

print("\n===== ORIGINAL PLAN =====\n")

original = engine.analyze_plan(
    drugs,
    age=70,
    kidney_disease=True
)

print(original["schedule"])


print("\n===== REMOVE IBUPROFEN =====\n")

scenario = engine.simulate_remove_drug(
    drugs,
    "Ibuprofen",
    age=70,
    kidney_disease=True
)

print(scenario["schedule"])