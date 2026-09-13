"""
Module de nettoyage des données des communes françaises.

Toutes les fonctions prennent un DataFrame en entrée et en renvoient un
nouveau (pas de modification "en place" cachée), pour que le pipeline
reste facile à suivre et à déboguer étape par étape.
"""

import json
from pathlib import Path

import pandas as pd


def load_raw_json(path: Path) -> pd.DataFrame:
    """Charge le JSON brut téléchargé par src/download.py dans un DataFrame."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renomme les colonnes brutes de l'API vers des noms clairs en français."""
    mapping = {
        "nom": "nom_commune",
        "code": "code_insee",
        "codeDepartement": "code_departement",
        "codeRegion": "code_region",
        "codesPostaux": "codes_postaux",
        "population": "population",
        "surface": "surface_km2",
        "centre.coordinates": "coordonnees",
    }
    existing = {k: v for k, v in mapping.items() if k in df.columns}
    return df.rename(columns=existing)


def split_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Éclate la colonne 'coordonnees' ([lon, lat]) en deux colonnes numériques."""
    df = df.copy()
    if "coordonnees" in df.columns:
        df["longitude"] = df["coordonnees"].apply(
            lambda c: c[0] if isinstance(c, list) and len(c) == 2 else pd.NA
        )
        df["latitude"] = df["coordonnees"].apply(
            lambda c: c[1] if isinstance(c, list) and len(c) == 2 else pd.NA
        )
        df = df.drop(columns=["coordonnees"])
    if "centre.type" in df.columns:
        df = df.drop(columns=["centre.type"])
    return df


def clean_codes_postaux(df: pd.DataFrame) -> pd.DataFrame:
    """Transforme la liste de codes postaux en une chaîne 'lisible', séparée par ';'."""
    df = df.copy()
    if "codes_postaux" in df.columns:
        df["codes_postaux"] = df["codes_postaux"].apply(
            lambda x: ";".join(x) if isinstance(x, list) else pd.NA
        )
    return df


def fix_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Force les bons types de colonnes (texte, entier, flottant)."""
    df = df.copy()
    if "population" in df.columns:
        df["population"] = pd.to_numeric(df["population"], errors="coerce").astype("Int64")
    if "surface_km2" in df.columns:
        df["surface_km2"] = pd.to_numeric(df["surface_km2"], errors="coerce")
    for col in ["code_insee", "code_departement", "code_region", "nom_commune"]:
        if col in df.columns:
            df[col] = df[col].astype("string")
    return df


def drop_incomplete_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Supprime les lignes sans code INSEE ou sans code département : ce sont
    des enregistrements inutilisables pour la suite du pipeline (ex : les
    arrondissements municipaux sans rattachement clair selon les champs demandés).
    """
    df = df.copy()
    before = len(df)
    df = df.dropna(subset=["code_insee", "code_departement"])
    after = len(df)
    if before != after:
        print(f"{before - after} ligne(s) incomplète(s) supprimée(s).")
    return df


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime les doublons éventuels sur le code INSEE (identifiant unique)."""
    df = df.copy()
    before = len(df)
    df = df.drop_duplicates(subset=["code_insee"])
    after = len(df)
    if before != after:
        print(f"{before - after} doublon(s) supprimé(s).")
    return df


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remet les colonnes dans un ordre logique et lisible."""
    order = [
        "code_insee",
        "nom_commune",
        "code_departement",
        "code_region",
        "codes_postaux",
        "population",
        "surface_km2",
        "latitude",
        "longitude",
    ]
    existing = [c for c in order if c in df.columns]
    remaining = [c for c in df.columns if c not in existing]
    return df[existing + remaining]


def clean_pipeline(raw_json_path: Path) -> pd.DataFrame:
    """
    Enchaîne toutes les étapes de nettoyage dans l'ordre.
    C'est LA fonction à appeler depuis les scripts.
    """
    df = load_raw_json(raw_json_path)
    df = rename_columns(df)
    df = split_coordinates(df)
    df = clean_codes_postaux(df)
    df = fix_dtypes(df)
    df = drop_incomplete_rows(df)
    df = drop_duplicates(df)
    df = reorder_columns(df)
    df = df.sort_values("code_insee").reset_index(drop=True)
    return df
