"""
Module de téléchargement des données des communes françaises.

Source : geo.api.gouv.fr (API publique, gratuite, sans clé nécessaire),
basée sur le Code Officiel Géographique (COG) de l'INSEE.

Documentation de l'API : https://geo.api.gouv.fr/decoupage-administratif/communes
"""

import json
from pathlib import Path

import requests

# Champs demandés à l'API. On en prend large, on filtrera au nettoyage.
FIELDS = [
    "nom",
    "code",
    "codeDepartement",
    "codeRegion",
    "codesPostaux",
    "population",
    "surface",
    "centre",
]

API_URL = "https://geo.api.gouv.fr/communes"


def download_communes(output_path: Path, fields: list[str] | None = None) -> Path:
    """
    Télécharge la liste complète des communes françaises depuis l'API
    et enregistre la réponse brute en JSON (sans aucune transformation).

    Parameters
    ----------
    output_path : Path
        Chemin du fichier JSON de sortie (ex: data/raw/communes_raw.json)
    fields : list[str], optional
        Liste des champs à demander à l'API. Par défaut FIELDS.

    Returns
    -------
    Path
        Le chemin du fichier créé.
    """
    fields = fields or FIELDS
    params = {
        "fields": ",".join(fields),
        "format": "json",
        "geometry": "centre",
    }

    print(f"Téléchargement depuis {API_URL} ...")
    response = requests.get(API_URL, params=params, timeout=60)
    response.raise_for_status()  # lève une erreur claire si le serveur répond mal

    data = response.json()
    print(f"{len(data)} communes récupérées.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Données brutes enregistrées dans : {output_path}")
    return output_path


if __name__ == "__main__":
    # Permet de tester ce module isolément avec : python src/download.py
    project_root = Path(__file__).resolve().parents[1]
    download_communes(project_root / "data" / "raw" / "communes_raw.json")
