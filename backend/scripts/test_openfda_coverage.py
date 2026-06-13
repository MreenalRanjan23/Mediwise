import pandas as pd
import requests


FILE = "data/processed/final/drug_metadata_chemical_v1.csv"

df = pd.read_csv(FILE)

df = df.head(100)


success = 0


for drug in df["generic_name"]:

    drug = str(drug).strip()

    queries = [

        f'openfda.generic_name:"{drug}"',

        f'openfda.substance_name:"{drug}"',

        f'openfda.brand_name:"{drug}"',

        drug
    ]

    found = False

    for q in queries:

        try:

            url = (
                "https://api.fda.gov/drug/label.json"
                f"?search={q}"
                "&limit=1"
            )

            r = requests.get(
                url,
                timeout=10
            )

            if r.status_code == 200:

                found = True
                break

        except:
            pass

    if found:
        success += 1


print("\n")
print("=" * 50)

print(
    f"Matched: {success}"
)

print(
    f"Coverage: {(success/100)*100:.2f}%"
)