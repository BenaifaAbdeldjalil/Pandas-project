import pandas as pd
import json
from pathlib import Path


f=Path("data/raw/communes_raw.json")

                      # Écrire directement la réponse JSON dans un fichier
with open(f, "r", encoding="utf-8") as f:
                
                data=json.load(f)

data_normalise=pd.json_normalize(data)
print(data_normalise)





