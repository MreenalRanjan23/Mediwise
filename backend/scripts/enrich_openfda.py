import pandas as pd
import requests
from tqdm import tqdm


INPUT_FILE = "data/processed/final/drug_metadata_chemical_v1.csv"

OUTPUT_FILE = "data/processed/drug_metadata_openfda.csv"


# ==================================================
# LOAD DATASET
# ==================================================

df = pd.read_csv(INPUT_FILE)

# ==================================================
# TEST MODE
# Uncomment for quick testing
# ==================================================

# df = df.head(100)

# For full run use:
# df = df

rows = []

matched_count = 0
unmatched_count = 0


# ==================================================
# OPENFDA SEARCH
# ==================================================

def get_openfda_record(drug_name):

    queries = [

        f'openfda.generic_name:"{drug_name}"',

        f'openfda.substance_name:"{drug_name}"',

        f'openfda.brand_name:"{drug_name}"',

        drug_name
    ]

    for query in queries:

        try:

            url = (
                "https://api.fda.gov/drug/label.json"
                f"?search={query}"
                "&limit=1"
            )

            response = requests.get(
                url,
                timeout=10
            )

            if response.status_code == 200:

                data = response.json()

                if "results" in data:

                    return data["results"][0]

        except Exception:
            pass

    return None


# ==================================================
# ENRICHMENT LOOP
# ==================================================

for _, row in tqdm(
    df.iterrows(),
    total=len(df)
):

    drug = str(
        row["generic_name"]
    ).strip()

    row_dict = row.to_dict()

    try:

        result = get_openfda_record(drug)

        if result is None:

            unmatched_count += 1

            row_dict.update({

                "boxed_warning": None,

                "warnings": None,

                "warnings_and_cautions": None,

                "contraindications": None,

                "adverse_reactions": None,

                "drug_interactions": None,

                "indications_and_usage": None,

                "pregnancy": None,

                "use_in_specific_populations": None
            })

            rows.append(row_dict)

            continue

        matched_count += 1

        row_dict.update({

            "boxed_warning":

                " ".join(
                    result.get(
                        "boxed_warning",
                        []
                    )
                ),

            "warnings":

                " ".join(
                    result.get(
                        "warnings",
                        []
                    )
                ),

            "warnings_and_cautions":

                " ".join(
                    result.get(
                        "warnings_and_cautions",
                        []
                    )
                ),

            "contraindications":

                " ".join(
                    result.get(
                        "contraindications",
                        []
                    )
                ),

            "adverse_reactions":

                " ".join(
                    result.get(
                        "adverse_reactions",
                        []
                    )
                ),

            "drug_interactions":

                " ".join(
                    result.get(
                        "drug_interactions",
                        []
                    )
                ),

            "indications_and_usage":

                " ".join(
                    result.get(
                        "indications_and_usage",
                        []
                    )
                ),

            "pregnancy":

                " ".join(
                    result.get(
                        "pregnancy",
                        []
                    )
                ),

            "use_in_specific_populations":

                " ".join(
                    result.get(
                        "use_in_specific_populations",
                        []
                    )
                )
        })

        rows.append(row_dict)

    except Exception:

        unmatched_count += 1

        row_dict.update({

            "boxed_warning": None,

            "warnings": None,

            "warnings_and_cautions": None,

            "contraindications": None,

            "adverse_reactions": None,

            "drug_interactions": None,

            "indications_and_usage": None,

            "pregnancy": None,

            "use_in_specific_populations": None
        })

        rows.append(row_dict)


# ==================================================
# SAVE OUTPUT
# ==================================================

output = pd.DataFrame(rows)

output.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n")
print("=" * 60)
print("OPENFDA ENRICHMENT COMPLETE")
print("=" * 60)

print(
    f"Total Drugs: {len(output)}"
)

print(
    f"Matched: {matched_count}"
)

print(
    f"Unmatched: {unmatched_count}"
)

print(
    f"Coverage: {(matched_count / len(output)) * 100:.2f}%"
)

print("\nSaved:")

print(OUTPUT_FILE)