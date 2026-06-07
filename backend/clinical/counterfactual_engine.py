from clinical.risk_aggregator import RiskAggregator
from clinical.scheduler import MedicationScheduler


class CounterfactualEngine:

    def __init__(self, metadata_path, interaction_path):

        self.risk_engine = RiskAggregator(
            metadata_path,
            interaction_path
        )

        self.scheduler = MedicationScheduler(
            metadata_path,
            interaction_path
        )

    # ------------------------------------
    # Utility: Normalize drug list
    # ------------------------------------
    def _normalize_drugs(self, drugs):
        return [d.strip().lower() for d in drugs if d]

    # ------------------------------------
    # Base analysis
    # ------------------------------------
    def analyze_plan(self, drugs, patient_profile):

        drugs = self._normalize_drugs(drugs)

        if not drugs:
            return {
                "drugs": [],
                "risk_analysis": {},
                "schedule": "No drugs provided"
            }

        # Risk analysis
        risk = self.risk_engine.analyze_medication_plan(
            drugs,
            patient_profile
        )

        # Schedule generation
        schedule_report = self.scheduler.generate_daily_report(drugs)

        return {
            "drugs": drugs,
            "risk_analysis": risk,
            "schedule": schedule_report
        }

    # ------------------------------------
    # Scenario: Remove a drug
    # ------------------------------------
    def simulate_remove_drug(self, drugs, remove_drug, patient_profile):

        drugs = self._normalize_drugs(drugs)
        remove_drug = remove_drug.strip().lower()

        new_drugs = [d for d in drugs if d != remove_drug]

        return self.analyze_plan(
            new_drugs,
            patient_profile
        )

    # ------------------------------------
    # Scenario: Add a drug
    # ------------------------------------
    def simulate_add_drug(self, drugs, new_drug, patient_profile):

        drugs = self._normalize_drugs(drugs)
        new_drug = new_drug.strip().lower()

        if new_drug not in drugs:
            drugs.append(new_drug)

        return self.analyze_plan(
            drugs,
            patient_profile
        )

    # ------------------------------------
    # Scenario: Replace a drug
    # ------------------------------------
    def simulate_replace_drug(self, drugs, old_drug, new_drug, patient_profile):

        drugs = self._normalize_drugs(drugs)
        old_drug = old_drug.strip().lower()
        new_drug = new_drug.strip().lower()

        new_drugs = [
            new_drug if d == old_drug else d
            for d in drugs
        ]

        return self.analyze_plan(
            new_drugs,
            patient_profile
        )