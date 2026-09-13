import requests
import json

url = "https://geo.api.gouv.fr/communes"
base="data/raw/"

FIELDS = [
    "nom",
    "code",
    "codeDepartement",
    "codeRegion",
    "population",
    "surface",
    "codesPostaux",
    "siren",
]

params = {
    "fields": ",".join(FIELDS),   # liste → "nom,code,codeDepartement"
    "format": "json",
     "zone": "metro,drom,com",     # métropole + DROM + COM
    }



response = requests.get(url, params=params, timeout=30)
            # Vérifier que la requête a réussi
if response.raise_for_status() is None:
                # Écrire directement la réponse JSON dans un fichier
    with open(f"{base}communes_raw.json", "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=4, ensure_ascii=False)
