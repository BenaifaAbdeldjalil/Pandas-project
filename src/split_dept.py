import pandas as pd
import json
from pathlib import Path
import numpy as np

#split by departement
def split_dep(df: pd.DataFrame, output_dir: Path):

    output_dir.mkdir(parents=True, exist_ok=True)
    created_files = []

    for code_dept, group in df.groupby("cp"):
        file_path = output_dir / f"departement_{code_dept}.csv"
        group.to_csv(file_path, index=False, encoding="utf-8")
        created_files.append(file_path)

    print(f"{len(created_files)} file département created in {output_dir}")
    return created_files



def compute_stats_departements(df: pd.DataFrame) :
    stats = (
        df.groupby("cp")
        .agg(
            nb_communes=("code insee", "count"),
            population_totale=("population", "sum"),
            surface_totale_km2=("surface", "sum"),
        )
        .reset_index()
    )
    stats["densite_hab_km2"] = (
        stats["population_totale"] / stats["surface_totale_km2"]
    ).round(1)
    stats = stats.sort_values("cp").reset_index(drop=True)
    return stats

