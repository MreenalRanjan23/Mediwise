import pandas as pd


class PrescriptionParser:

    def __init__(self, metadata_path):

        df = pd.read_csv(metadata_path)

        self.drugs = set(df["drug_name"].str.lower())

    def extract_drugs(self, text):

        text = text.lower()

        words = text.replace(",", " ").replace("\n", " ").split()

        found_drugs = set()

        for word in words:

            if word in self.drugs:
                found_drugs.add(word.capitalize())

        return list(found_drugs)