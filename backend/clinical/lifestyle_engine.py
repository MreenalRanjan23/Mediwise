class LifestyleEngine:

    def get_penalty(self, drug, patient_profile):

        penalty = 0
        reasons = []

        drug_lower = drug.lower()

        # -----------------------------
        # Smoking
        # -----------------------------
        if patient_profile.smoker:
            penalty += 5
            reasons.append("Smoking may alter drug metabolism")

        # -----------------------------
        # Alcohol
        # -----------------------------
        if patient_profile.alcohol_use:
            penalty += 10
            reasons.append("Alcohol increases liver toxicity risk")

        # -----------------------------
        # Occupation risk
        # -----------------------------
        if patient_profile.occupation:
            occupation = patient_profile.occupation.lower()

            if "driver" in occupation or "machine" in occupation:
                # crude rule: sedative-like drugs
                if any(x in drug_lower for x in ["diazepam", "alprazolam", "sleep", "sedative"]):
                    penalty += 40
                    reasons.append("Sedative drugs unsafe for driving/operating machinery")

        return penalty, reasons