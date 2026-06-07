from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import TanimotoSimilarity


class SimilarityEngine:

    def __init__(self, metadata_path):

        import pandas as pd
        self.df = pd.read_csv(metadata_path)

        # Precompute fingerprints
        self.fingerprints = {}

        for _, row in self.df.iterrows():

            drug = row["drug_name"]
            smiles = row.get("smiles", None)

            if isinstance(smiles, str) and smiles:

                mol = Chem.MolFromSmiles(smiles)

                if mol:
                    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
                    self.fingerprints[drug.lower()] = fp

    # -----------------------------
    # Compute similarity
    # -----------------------------
    def similarity(self, drug_a, drug_b):

        fp1 = self.fingerprints.get(drug_a.lower())
        fp2 = self.fingerprints.get(drug_b.lower())

        if not fp1 or not fp2:
            return 0

        return TanimotoSimilarity(fp1, fp2)

    # -----------------------------
    # Get similar drugs
    # -----------------------------
    def get_similar_drugs(self, drug, top_n=3):

        target_fp = self.fingerprints.get(drug.lower())

        if not target_fp:
            return []

        scores = []

        for d, fp in self.fingerprints.items():

            if d == drug.lower():
                continue

            score = TanimotoSimilarity(target_fp, fp)

            scores.append((d, score))

        scores.sort(key=lambda x: x[1], reverse=True)

        return scores[:top_n]