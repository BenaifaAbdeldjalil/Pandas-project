"""
ÉTAPE 3 — Découpage des données en un fichier CSV par département.

Prérequis : avoir lancé 02_clean_data.py avant.

Usage :
    python scripts/03_split_by_departement.py

Résultat :
    data/final/by_departement/{code_departement}.csv  (un fichier par département)
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.split_dept import split_by_departement

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_INPUT = PROJECT_ROOT / "data" / "processed" / "communes_clean.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "final" / "by_departement"


def main():
    if not CLEAN_INPUT.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {CLEAN_INPUT}\n"
            "As-tu bien lancé 'python scripts/02_clean_data.py' avant ?"
        )

    df = pd.read_csv(CLEAN_INPUT, dtype={"code_departement": "string"})
    split_by_departement(df, OUTPUT_DIR)


if __name__ == "__main__":
    main()
