"""
ÉTAPE 1 — Téléchargement des données brutes.

Usage :
    python scripts/01_download_data.py

Résultat :
    data/raw/communes_raw.json
"""

import sys
from pathlib import Path

# Permet d'importer le package src/ depuis n'importe où
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.download import download_communes

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_OUTPUT = PROJECT_ROOT / "data" / "raw" / "communes_raw.json"


def main():
    download_communes(RAW_OUTPUT)


if __name__ == "__main__":
    main()
