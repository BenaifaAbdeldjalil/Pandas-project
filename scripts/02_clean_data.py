from pathlib import Path
import sys


# Permet d'importer le package src/ depuis n'importe où
sys.path.append(str(Path(__file__).resolve().parents[1]))

#import clean modul from SRC folder
from src.clean import clean_data

f=Path("data/raw/communes_raw.json")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_INPUT = PROJECT_ROOT / "data" / "raw" / "communes_raw.json"
CSV_OUTPUT = PROJECT_ROOT / "data" / "processed" / "communes_clean.csv"
# PARQUET_OUTPUT = PROJECT_ROOT / "data" / "processed" / "communes_clean.parquet"


def main():
    if not RAW_INPUT.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {RAW_INPUT}\n"
            "As-tu bien lancé 'python scripts/01_download_data.py' avant ?"
        )

    print("Nettoyage des données en cours...")
    df = clean_data(RAW_INPUT)

    CSV_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_OUTPUT, index=False, encoding="utf-8")
   #  df.to_parquet(PARQUET_OUTPUT, index=False)

    print(f"{len(df)} communes cleans.")
    print(f"→ {CSV_OUTPUT}")
    # print(f"→ {PARQUET_OUTPUT}")
    print("\nAperçu :")
    print(df.head())


if __name__ == "__main__":
    main()


