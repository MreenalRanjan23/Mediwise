import pandas as pd

FILE = "data/processed/drug_metadata.csv"

df = pd.read_csv(FILE)

missing = df[
    df["smiles"].isna()
]

print("\n")
print("=" * 50)
print("MISSING SMILES REPORT")
print("=" * 50)

print(f"Total missing: {len(missing)}")

print("\nFirst 100 Missing Drugs:\n")

for drug in missing["generic_name"].head(100):
    print(drug)

missing.to_csv(
    "data/processed/missing_smiles.csv",
    index=False
)

print("\nSaved:")
print("data/processed/missing_smiles.csv")