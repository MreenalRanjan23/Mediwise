import pandas as pd

FILE = "data/processed/drug_metadata_openfda.csv"

df = pd.read_csv(FILE)

clinical_columns = [

    "boxed_warning",
    "warnings",
    "warnings_and_cautions",
    "contraindications",
    "adverse_reactions",
    "drug_interactions",
    "pregnancy",
    "use_in_specific_populations"
]

print("\n")
print("=" * 60)
print("CLINICAL COVERAGE REPORT")
print("=" * 60)

for col in clinical_columns:

    count = df[col].notna().sum()

    coverage = (
        count / len(df)
    ) * 100

    print(
        f"{col}: {coverage:.2f}%"
    )