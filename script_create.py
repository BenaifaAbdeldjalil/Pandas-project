import os
from pathlib import Path

folders = ["data","scripts","src","data/raw/","data/processed/","data/final/"]

base = Path(".")


base = Path(".")  # dossier courant
# 1) folders creation
for f in folders:
    path = base / f
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Créé : {path}")
    else:
        print(f"⏭️  Existe déjà : {path}")

print("\nContenu actuel :", os.listdir())

files = ["data/processed/test.txt","data/raw/test.txt",
         "scripts/01_download_data.py","scripts/02_clean_data.py",
         "scripts/03_split_by_departement.py","scripts/04_stats_departements.py",
         "src/clean.py","src/download.py",
         "src/split_dept.py"]
# 2) files creation
for fi in files:
    file = base/fi
    if file.exists():
        print(f"⏭️  Le fichier { file } existe déjà")
    else:
        file.write_text("Hello\n", encoding="utf-8")
        print(f"✅ Fichier créé : { file.resolve() }")