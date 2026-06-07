import requests

drug = "tobramycin"

url = (
    f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
    f"compound/name/{drug}/property/"
    f"MolecularFormula,"
    f"MolecularWeight,"
    f"ConnectivitySMILES/JSON"
)

data = requests.get(url).json()

print(data)