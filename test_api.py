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
print(df.columns)
df["code Postal"]=df["codesPostaux"].astype(str).str.strip().str.zfill(5)
df["code Postal"]=df["code Postal"].str.replace("[^0-9]","",regex=True)
df["code Postal 2"]=pd.to_numeric(df["code Postal"])


    #duplicate row
df["cp"] = np.where(
    df["code Postal 2"] < 96000,
    df["code Postal"].str[:2],
    df["code Postal"].str[:3]
)

print(df.columns)

stats = (
    df.groupby("cp")
    .agg(
        nb_communes=("code", "count"),
        population_totale=("population", "sum"),
        surface_totale_km2=("surface", "sum"),
    )
    .reset_index()
)
stats["densite_hab_km2"] = (
    stats["population_totale"] / stats["surface_totale_km2"]
).round(1)
stats = stats.sort_values("cp").reset_index(drop=True)

print(stats)
