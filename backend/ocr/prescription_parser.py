import re


COMMON_DRUGS = [
    "paracetamol",
    "ibuprofen",
    "aspirin",
    "naproxen",
    "diclofenac",
    "amoxicillin",
    "metformin",
    "atorvastatin"
]


class PrescriptionParser:

    def extract_medications(self, text):

        text_lower = text.lower()

        medications = []

        for drug in COMMON_DRUGS:

            if drug in text_lower:

                dosage_match = re.search(
                    rf"{drug}\s*(\d+mg)",
                    text_lower
                )

                dosage = (
                    dosage_match.group(1)
                    if dosage_match
                    else "Unknown"
                )

                medications.append({
                    "drug": drug,
                    "dosage": dosage
                })

        return medications