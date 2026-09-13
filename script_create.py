import os
from pathlib import Path

folders = ["data","src","data/raw/","data/processed/","data/final/"]

base = Path(".")


base = Path(".")  # dossier courant

for f in folders:
    path = base / f
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Créé : {path}")
    else:
        print(f"⏭️  Existe déjà : {path}")

print("\nContenu actuel :", os.listdir())


# 2) Créer test.txt dans data/processed
fichier = base / "data/processed/test.txt"
fichier.write_text("Hello\n", encoding="utf-8")

print(f"✅ Fichier créé : {fichier.resolve()}")