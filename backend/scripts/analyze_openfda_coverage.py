import pandas as pd

FILE = "data/processed/drug_metadata_openfda.csv"

df = pd.read_csv(FILE)

warnings_count = df["warnings"].notna().sum()
contra_count = df["contraindications"].notna().sum()
adverse_count = df["adverse_reactions"].notna().sum()

print("\nOPENFDA COVERAGE REPORT")
print("=" * 50)

print(f"Total Drugs: {len(df)}")
print(f"Warnings Found: {warnings_count}")
print(f"Contraindications Found: {contra_count}")
print(f"Adverse Reactions Found: {adverse_count}")

print("\nCoverage %")

print(
    f"Warnings: {(warnings_count/len(df))*100:.2f}%"
)

print(
    f"Contraindications: {(contra_count/len(df))*100:.2f}%"
)

print(
    f"Adverse Reactions: {(adverse_count/len(df))*100:.2f}%"
)