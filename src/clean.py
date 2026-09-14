import pandas as pd
import json
from pathlib import Path
import numpy as np


def load_data(path:Path):
                      # Écrire directement la réponse JSON dans un fichier
        with open(path, "r", encoding="utf-8") as f:              
                data=json.load(f)
        data_normalise=pd.json_normalize(data)
        return data_normalise


def fill_data(dataframe):
    df =dataframe
    #make name upper
    df["nom"]=df["nom"].str.upper()

    #fill NAN with ""
    df=df.astype(str).fillna("")
    return df


def rename_data(dataframe):
    df =dataframe
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
    return df


def cleaning_data(dataframe):
    df =dataframe
    #cleaning postal code 
    df["code Postal"]=df["code Postal"].str.replace("[^0-9]","",regex=True)
    return df


def convert_data(dataframe):
    df =dataframe
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
    return df


def null_data(dataframe):
    df =dataframe
    #drop na
    df = df.dropna(subset=["code insee", "code Departement"])
    return df


def duplicale_data(dataframe):
    df =dataframe
    #duplicate row
    df=df.drop_duplicates(subset=["code insee"])

    return df

def calculate_data(dataframe):
    df =dataframe
    #
    df["population"]=pd.to_numeric(df["population"],errors="coerce")
    df["surface"] = pd.to_numeric(df["surface"],errors="coerce")
    df["density"]=df["population"]/df["surface"] 

    return df


def cp_data(dataframe):
    df =dataframe
    df["cp"] = np.where(
    df["code Postal 2"] < 96000,
    df["code Postal"].str[:2],
    df["code Postal"].str[:3]
)
    return df


def clean_data(f):
     dataframe=load_data(f)
     dataframe=fill_data(dataframe)
     dataframe=rename_data(dataframe)
     dataframe=cleaning_data(dataframe)
     dataframe=convert_data(dataframe)
     dataframe=null_data(dataframe)
     dataframe=duplicale_data(dataframe)
     dataframe=calculate_data(dataframe)
     dataframe=cp_data(dataframe)
     print(dataframe)
     return dataframe
