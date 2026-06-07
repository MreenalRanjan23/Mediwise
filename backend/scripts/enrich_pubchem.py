import pandas as pd
import requests
from tqdm import tqdm


INPUT_FILE = "data/external/drug_list_raw.csv"
OUTPUT_FILE = "data/processed/drug_metadata.csv"


# ==================================================
# LOAD DRUG LIST
# ==================================================

df = pd.read_csv(
    INPUT_FILE,
    names=[
        "drug_id",
        "drug_name"
    ]
)

# --------------------------------------------------
# TEMP TESTING
# Uncomment for quick validation on 5 drugs
# --------------------------------------------------
# df = df.head(5)

rows = []


# ==================================================
# PUBCHEM ENRICHMENT
# ==================================================

for _, row in tqdm(
    df.iterrows(),
    total=len(df)
):

    drug = str(
        row["drug_name"]
    ).strip()

    try:

        url = (
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
            f"compound/name/{drug}/property/"
            f"MolecularFormula,"
            f"MolecularWeight,"
            f"ConnectivitySMILES"
            f"/JSON"
        )

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:

            rows.append({

                "drug_id":
                    row["drug_id"],

                "generic_name":
                    drug,

                "molecular_formula":
                    None,

                "molecular_weight":
                    None,

                "smiles":
                    None
            })

            continue

        data = response.json()

        props = data[
            "PropertyTable"
        ]["Properties"][0]

        rows.append({

            "drug_id":
                row["drug_id"],

            "generic_name":
                drug,

            "molecular_formula":
                props.get(
                    "MolecularFormula"
                ),

            "molecular_weight":
                props.get(
                    "MolecularWeight"
                ),

            "smiles":
                props.get(
                    "ConnectivitySMILES"
                )
        })

    except Exception as e:

        rows.append({

            "drug_id":
                row["drug_id"],

            "generic_name":
                drug,

            "molecular_formula":
                None,

            "molecular_weight":
                None,

            "smiles":
                None
        })


# ==================================================
# SAVE OUTPUT
# ==================================================

output = pd.DataFrame(
    rows
)

output.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nSaved: {OUTPUT_FILE}"
)

print(
    f"Total drugs processed: {len(output)}"
)

print(
    f"SMILES found: {output['smiles'].notna().sum()}"
)

print(
    f"SMILES missing: {output['smiles'].isna().sum()}"
)