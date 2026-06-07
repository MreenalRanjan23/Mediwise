import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from clinical.risk_aggregator import RiskAggregator

engine = RiskAggregator(
    "data/raw/drug_metadata.csv",
    "data/raw/drug_interactions.csv"
)

drugs = ["Warfarin", "Ibuprofen", "Paracetamol"]

result = engine.analyze_medication_plan(
    drugs,
    age=70,
    kidney_disease=True
)

print(result)