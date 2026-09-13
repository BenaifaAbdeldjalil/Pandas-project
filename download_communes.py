import requests
import json

def download_communes(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status() 
            # Vérifier que la requête a réussi
        if response.raise_for_status() is None:
            data = response.json()

                # Écrire directement la réponse JSON dans un fichier
            with open("data/raw/communes_raw.json", "w", encoding="utf-8") as f:
                json.dump(response.json(), f, indent=4, ensure_ascii=False)
                    
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erreur HTTP : {e}")
    except requests.exceptions.Timeout:
        print("❌ Délai dépassé (timeout)")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur réseau : {e}")
    except OSError as e:
        print(f"❌ Erreur d'écriture fichier : {e}")

url1 = "https://geo.api.gouv.fr/communes?fields=nom,code,codeDepartement,population"
download_communes(url1)