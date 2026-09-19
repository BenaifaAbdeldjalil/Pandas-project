import pandas as pd
import json
from pathlib import Path
import numpy as np

f=Path("data/raw/communes_raw.json")

                      # Écrire directement la réponse JSON dans un fichier
with open(f, "r", encoding="utf-8") as f:
                
                data=json.load(f)

df=pd.json_normalize(data)
#print(df)

df=df[:10].copy()
df["code Postal"]=df["code Postal"].astype(str).str.strip().str.zfill(5)
df["code Postal"]=df["code Postal"].str.replace("[^0-9]","",regex=True)
df["code Postal 2"]=pd.to_numeric(df["code Postal"])


    #duplicate row
df["cp"] = np.where(
    df["code Postal 2"] < 96000,
    df["code Postal"].str[:2],
    df["code Postal"].str[:3]
)

print(df)
