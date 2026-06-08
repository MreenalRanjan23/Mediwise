import pandas as pd


FILE = "data/processed/missing_smiles.csv"

df = pd.read_csv(FILE)

categories = {
    "biologics_mab": [],
    "proteins_hormones": [],
    "polymers": [],
    "radiopharmaceuticals": [],
    "gene_therapy": [],
    "others": []
}


for drug in df["generic_name"]:

    drug = str(drug).lower().strip()

    # Monoclonal antibodies
    if drug.endswith("mab"):
        categories["biologics_mab"].append(drug)

    # Proteins / hormones / enzymes
    elif (
        drug.endswith("alfa")
        or drug.endswith("ase")
        or drug.endswith("tide")
        or drug.endswith("stim")
        or drug.endswith("tropin")
        or drug.endswith("kinase")
        or "hormone" in drug
    ):
        categories["proteins_hormones"].append(drug)

    # Polymers / excipients
    elif (
        drug.startswith("poly")
        or "poly" in drug
        or "dextrin" in drug
        or "povidone" in drug
        or "trimethicone" in drug
    ):
        categories["polymers"].append(drug)

    # Radioactive agents
    elif (
        "technetium" in drug
        or "radium" in drug
        or "tc 99" in drug
    ):
        categories["radiopharmaceuticals"].append(drug)

    # Gene therapies
    elif (
        "abeparvovec" in drug
        or "gene" in drug
    ):
        categories["gene_therapy"].append(drug)

    else:
        categories["others"].append(drug)


print("\n")
print("=" * 60)
print("MISSING SMILES CLASSIFICATION REPORT")
print("=" * 60)

total = 0

for category, drugs in categories.items():

    count = len(drugs)

    total += count

    print(f"\n{category.upper()}: {count}")

    for d in drugs[:10]:
        print("  -", d)

print("\n")
print("=" * 60)
print(f"TOTAL CLASSIFIED: {total}")
print("=" * 60)


# Save categorized CSVs

for category, drugs in categories.items():

    pd.DataFrame(
        {"drug_name": drugs}
    ).to_csv(
        f"data/processed/{category}.csv",
        index=False
    )

print("\nSaved category files to:")
print("data/processed/")