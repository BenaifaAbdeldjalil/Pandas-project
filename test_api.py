import requests
import json








url = "https://geo.api.gouv.fr/communes?fields=nom,code,codeDepartement,population"
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status() 
        # Vérifier que la requête a réussi
    print(response.raise_for_status() )
    if response.raise_for_status() is None:
        data = response.json()

            # Écrire directement la réponse JSON dans un fichier
        with open("data/raw/communes_raw.json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)
                
except:
        print("error")


