import requests
import json
from pathlib import Path
import sys


# Permet d'importer le package src/ depuis n'importe où
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Permet d'importer le package src/ depuis n'importe où
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.download import download_communes


url="https://geo.api.gouv.fr/communes"
base="data/raw/"


def main():
    download_communes(url,base)


if __name__ == "__main__":
    main()


