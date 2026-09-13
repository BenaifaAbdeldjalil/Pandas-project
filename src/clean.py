import pandas as pd
import json
from pathlib import Path


def load_data(path:Path):
                      # Écrire directement la réponse JSON dans un fichier
        with open(path, "r", encoding="utf-8") as f:              
                data=json.load(f)
        data_normalise=pd.json_normalize(data)
        return data_normalise


def clean_data(dataframe):
    df =dataframe

    #make name upper
    df["nom"]=df["nom"].str.upper()

    #fill NAN with ""
    df=df.astype(str).fillna("")

    #rename column 
    new_column={
            "nom": "nom commune",
            "code": "code insee",
            "codeDepartement": "code Departement",
            "surface": "surface",
            "codesPostaux": "code Postal",
            "siren": "siren",
            "codeRegion": "code Region",
            "population": "population",
    }
    df.rename(columns=new_column,inplace=True)


    #cleaning postal code 
    df["code Postal"]=df["code Postal"].str.replace("[^0-9]","",regex=True)

    #string type
    for col in ["nom commune", "code insee", "code Departement", "code Region","code Postal"]:
        if col in df.columns:
            df[col] = df[col].astype(str)

    #numeric type
    for col in ["siren", "population"]:
        if col in df.columns:
            pd.to_numeric(df[col],errors="coerce")

    #float type 
    df["surface"] = df["surface"].astype(float)

    #drop na
    df = df.dropna(subset=["code insee", "code Departement"])

    #duplicate row
    df=df.drop_duplicates(subset=["code insee"])

    return df

