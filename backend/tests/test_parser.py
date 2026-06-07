import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clinical.prescription_parser import PrescriptionParser


parser = PrescriptionParser("data/raw/drug_metadata.csv")

text = """
Tab Warfarin 5 mg OD
Tab Ibuprofen 400 mg TID
Tab Paracetamol 500 mg PRN
"""

print(parser.extract_drugs(text))