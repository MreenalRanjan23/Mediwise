import pandas as pd
import requests

FILE = "data/processed/final/drug_metadata_chemical_v1.csv"

df = pd.read_csv(FILE)

sample = df.head(50)

for drug in sample["generic_name"]:

    drug = str(drug).strip()

    query = f'openfda.generic_name:"{drug}"'

    url = (
        "https://api.fda.gov/drug/label.json"
        f"?search={query}"
        "&limit=1"
    )

    try:

        r = requests.get(url, timeout=10)

        print("\n------------------")
        print(drug)
        print("STATUS:", r.status_code)

        if r.status_code == 200:

            data = r.json()

            print(
                "HAS RESULTS:",
                "results" in data
            )

            if "results" in data:

                print(
                    "FIELDS:",
                    list(
                        data["results"][0].keys()
                    )[:10]
                )

    except Exception as e:

        print(drug)
        print(e)