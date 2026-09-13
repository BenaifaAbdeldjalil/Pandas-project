
import requests
import json
from pathlib import Path
import sys


# Permet d'importer le package src/ depuis n'importe où
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Permet d'importer le package src/ depuis n'importe où
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.clean import load_data,clean_data


f=Path("data/raw/communes_raw.json")


def main():
    df = load_data(f)
    clean_data(df)


if __name__ == "__main__":
    main()


