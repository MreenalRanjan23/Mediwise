import pandas as pd
from pubchempy import get_compounds
import time

INPUT_PATH = "data/raw/drug_metadata.csv"
OUTPUT_PATH = "data/raw/drug_metadata.csv"  # overwrite safely


def fetch_smiles(drug_name):
    try:
        compounds = get_compounds(drug_name, "name")

        if compounds:
            return compounds[0].canonical_smiles
        else:
            return None

    except Exception as e:
        print(f"Error fetching {drug_name}: {e}")
        return None


def main():

    df = pd.read_csv(INPUT_PATH)

    # Ensure smiles column exists
    if "smiles" not in df.columns:
        df["smiles"] = None

    print("\n🚀 Generating SMILES...\n")

    updated_count = 0

    for i, row in df.iterrows():

        drug = row["drug_name"]

        # Skip if already exists
        if pd.notna(row["smiles"]) and row["smiles"] != "":
            continue

        print(f"Processing: {drug}")

        smiles = fetch_smiles(drug)

        if smiles:
            df.at[i, "smiles"] = smiles
            print(f"✅ Found SMILES")
            updated_count += 1
        else:
            print(f"❌ Not found")

        time.sleep(0.2)  # avoid rate limits

    df.to_csv(OUTPUT_PATH, index=False)

    print("\n=========================")
    print(f"✅ Updated {updated_count} drugs")
    print("📁 Dataset saved")
    print("=========================\n")


if __name__ == "__main__":
    main()