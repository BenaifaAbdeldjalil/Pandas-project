"""
ÉTAPE 2 — Nettoyage des données brutes.

Prérequis : avoir lancé 01_download_data.py avant.

Usage :
    python scripts/02_clean_data.py

Résultat :
    data/processed/communes_clean.csv
    data/processed/communes_clean.parquet
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.clean import clean_pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_INPUT = PROJECT_ROOT / "data" / "raw" / "communes_raw.json"
CSV_OUTPUT = PROJECT_ROOT / "data" / "processed" / "communes_clean.csv"
PARQUET_OUTPUT = PROJECT_ROOT / "data" / "processed" / "communes_clean.parquet"


def main():
    if not RAW_INPUT.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {RAW_INPUT}\n"
            "As-tu bien lancé 'python scripts/01_download_data.py' avant ?"
        )

    print("Nettoyage des données en cours...")
    df = clean_pipeline(RAW_INPUT)

    CSV_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_OUTPUT, index=False, encoding="utf-8")
    df.to_parquet(PARQUET_OUTPUT, index=False)

    print(f"{len(df)} communes nettoyées.")
    print(f"→ {CSV_OUTPUT}")
    print(f"→ {PARQUET_OUTPUT}")
    print("\nAperçu :")
    print(df.head())


if __name__ == "__main__":
    main()
