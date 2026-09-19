import pandas as pd
import json
from pathlib import Path
import numpy as np

df =pd.read_csv("data/processed/communes_clean.csv")
print(df.sort_values(by='cp',ascending=False))

filtre = df['cp']=='1'
dfcp=df[filtre]
print(dfcp)
