import requests
url = "https://geo.api.gouv.fr/communes?fields=nom,code,codeDepartement,population"
response = requests.get(url,timeout=30)



statut = response.status_code
raise_statut = response.raise_for_status()
print(statut,raise_statut)
data = response.json()

print(data[:5])
