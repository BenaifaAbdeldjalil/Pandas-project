from pathlib import Path
import sys


# Permet d'importer le package src/ depuis n'importe où
sys.path.append(str(Path(__file__).resolve().parents[1]))

#import clean modul from SRC folder
from src.clean import clean_data

f=Path("data/raw/communes_raw.json")


def main():
    clean_data(f)


if __name__ == "__main__":
    main()


