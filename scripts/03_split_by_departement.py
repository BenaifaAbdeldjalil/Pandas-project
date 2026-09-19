from pathlib import Path
import sys
import pandas as pd

# Permet d'importer le package src/ depuis n'importe où
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Permet d'importer le package src/ depuis n'importe où
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.split_dept import split_dep,compute_stats_departements

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_INPUT = PROJECT_ROOT / "data" / "processed" / "communes_clean.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "final" / "by_departement"



def main():
    if not CLEAN_INPUT.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {CLEAN_INPUT}\n"
            "did you run : 'python scripts/02_clean_data.py' before ?"
        )

    df = pd.read_csv(CLEAN_INPUT, dtype={"code_departement": "string"})
    split_dep(df, OUTPUT_DIR)


if __name__ == "__main__":
    main()