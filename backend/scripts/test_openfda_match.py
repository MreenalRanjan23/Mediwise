import requests


drug = "tobramycin"


queries = [

    f'openfda.generic_name:"{drug}"',

    f'openfda.substance_name:"{drug}"',

    f'openfda.brand_name:"{drug}"',

    drug
]


for q in queries:

    url = (
        "https://api.fda.gov/drug/label.json"
        f"?search={q}"
        "&limit=1"
    )

    try:

        r = requests.get(
            url,
            timeout=10
        )

        print("\n")
        print("=" * 50)

        print(q)

        print(
            "STATUS:",
            r.status_code
        )

        if r.status_code == 200:

            data = r.json()

            print(
                "FOUND:",
                len(
                    data["results"]
                )
            )

    except Exception as e:

        print(e)