"""
Module de découpage des données par département et de calcul de
statistiques agrégées.
"""

from pathlib import Path

import pandas as pd


def split_by_departement(df: pd.DataFrame, output_dir: Path) -> list[Path]:
    """
    Écrit un fichier CSV par département dans output_dir.

    Exemple : data/final/by_departement/75.csv, 13.csv, 2A.csv, 971.csv ...
    (les départements corses '2A'/'2B' et les DOM '971'...'976' sont bien
    gérés puisque code_departement est une colonne texte).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    created_files = []

    for code_dept, group in df.groupby("code_departement"):
        file_path = output_dir / f"{code_dept}.csv"
        group.to_csv(file_path, index=False, encoding="utf-8")
        created_files.append(file_path)

    print(f"{len(created_files)} fichiers département créés dans {output_dir}")
    return created_files


def compute_stats_departements(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule, pour chaque département :
    - le nombre de communes
    - la population totale
    - la surface totale (km2)
    - la densité moyenne (habitants / km2)
    """
    stats = (
        df.groupby("code_departement")
        .agg(
            nb_communes=("code_insee", "count"),
            population_totale=("population", "sum"),
            surface_totale_km2=("surface_km2", "sum"),
        )
        .reset_index()
    )
    stats["densite_hab_km2"] = (
        stats["population_totale"] / stats["surface_totale_km2"]
    ).round(1)
    stats = stats.sort_values("code_departement").reset_index(drop=True)
    return stats
