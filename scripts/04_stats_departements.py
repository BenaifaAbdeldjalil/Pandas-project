"""
ÉTAPE 4 — Calcul des statistiques agrégées par département.

Prérequis : avoir lancé 02_clean_data.py avant (03 n'est pas requis pour ce script).

Usage :
    python scripts/04_stats_departements.py

Résultat :
    data/final/stats_departements.csv
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.split_dept import compute_stats_departements

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_INPUT = PROJECT_ROOT / "data" / "processed" / "communes_clean.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "final" / "stats_departements.csv"


def main():
    if not CLEAN_INPUT.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {CLEAN_INPUT}\n"
            "As-tu bien lancé 'python scripts/02_clean_data.py' avant ?"
        )

    df = pd.read_csv(CLEAN_INPUT, dtype={"code_departement": "string"})
    stats = compute_stats_departements(df)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    stats.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"Statistiques calculées pour {len(stats)} départements.")
    print(f"→ {OUTPUT_FILE}")
    print("\nTop 5 départements les plus peuplés :")
    print(stats.sort_values("population_totale", ascending=False).head())


if __name__ == "__main__":
    main()
