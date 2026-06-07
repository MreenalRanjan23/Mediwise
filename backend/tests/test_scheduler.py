import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clinical.scheduler import MedicationScheduler


scheduler = MedicationScheduler(
    "data/raw/drug_metadata.csv",
    "data/raw/drug_interactions.csv"
)

drugs = ["Ciprofloxacin", "Metformin", "Calcium"]

report = scheduler.generate_daily_report(drugs)

print(report)