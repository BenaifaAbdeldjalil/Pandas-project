# 🇫🇷 French Communes — Step-by-Step Guide

This guide walks you through building the project **module by module**,
explaining each file's purpose, the design decisions and the pitfalls to
watch for. Read it in order: each module builds on the previous one.

---

## Table of contents

1. [Prerequisites and setup](#1-prerequisites-and-setup)
2. [Step 1 — Downloading the data (`src/download.py`)](#2-step-1--downloading-the-data)
3. [Step 2 — Cleaning the data (`src/clean.py`)](#3-step-2--cleaning-the-data)
4. [Step 3 — Splitting by department (`src/split_dept.py`)](#4-step-3--splitting-by-department)
5. [Step 4 — Statistics by department (`src/stats.py`)](#5-step-4--statistics-by-department)
6. [Why this architecture?](#6-why-this-architecture)
7. [Verifying everything works](#7-verifying-everything-works)
8. [Common errors and fixes](#8-common-errors-and-fixes)
9. [Going further](#9-going-further)

---

## 1. Prerequisites and setup

```bash
# Create the project and enter it
mkdir commune-france-project && cd commune-france-project

# Virtual environment (isolates project dependencies)
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt
```

**Contents of `requirements.txt`:**

```
requests   # HTTP calls to the API
pandas     # data manipulation (DataFrame)
pyarrow    # Parquet read/write engine
```

> 💡 Design choice: `pandas` is the reference library for data
> manipulation in Python. `pyarrow` enables Parquet, a columnar format
> **5 to 10× faster** than CSV on read.

---

## 2. Step 1 — Downloading the data

**Script:** `python scripts/01_download_data.py`
**Reusable module:** `src/download.py`

### Principle

We query `https://geo.api.gouv.fr/communes` while explicitly requesting
only the fields we need (otherwise the API returns everything, including
very heavy geographic outlines).

```python
params = {"fields": "nom,code,codeDepartement,codeRegion,population,surface,codesPostaux,siren",
          "format": "json", "geometry": "centre"}
requests.get(API_URL, params=params, timeout=30)
```

### Key module points

| Element | Why |
|---|---|
| `timeout=30` | Never wait forever if the API hangs |
| `retries` loop with `time.sleep(2 * attempt)` | Handles transient network failures (progressive backoff) |
| **Raw, unmodified** save in `data/raw/` | Immutability principle: always keep the original source so the pipeline can be replayed |
| `ensure_ascii=False` | Preserves French accents (Échirolles, Nœux-les-Mines...) |

### Output

`data/raw/communes_raw.json` — ~35,000 communes, a little over 10 MB.

---

## 3. Step 2 — Cleaning the data

**Script:** `python scripts/02_clean_data.py`
**Reusable module:** `src/clean.py`

This is the most important step. The raw API data has three typical
problems:

### Problem 1 — camelCase column names

The API returns `codeDepartement`, `codesPostaux`... We rename everything
to `snake_case` via a mapping dictionary:

```python
COLS_RENAME = {
    "codeDepartement": "code_departement",
    "codesPostaux": "codes_postaux",
    ...
}
df = df.rename(columns=COLS_RENAME)
```

### Problem 2 — Codes are strings, not numbers

⚠️ **Classic pitfall:** if pandas reads `code_commune` as an integer,
`"01001"` becomes `1001` and department `"01"` becomes `1`. We therefore
force the `string` type (and `str` on read):

```python
df["code_departement"] = df["code_departement"].astype("string").str.strip()
```

### Problem 3 — Missing values and mixed types

| Field | Treatment |
|---|---|
| `population` | `pd.to_numeric(..., errors="coerce")` + `Int64` type (**nullable** integer: pandas accepts `NA` without converting everything to float) |
| `surface` | Converted to float, renamed `surface_ha` (the API unit is hectares) |
| `codesPostaux` (list) | Flattened to `"13001,13002"` + extraction of a `code_postal_principal` |
| Missing `codeDepartement` | Filled with `"NA"` (some collectivities have no department) |

Finally: **deduplication** on `code_commune` (unique key) + **sorting**.

### Outputs

- `data/processed/communes_clean.csv`
- `data/processed/communes_clean.parquet` (10× faster to read afterwards)

---

## 4. Step 3 — Splitting by department

**Script:** `python scripts/03_split_by_departement.py`
**Reusable module:** `src/split_dept.py`

One single idea: `groupby("code_departement")`, then a loop writing one
CSV per group:

```python
for dept, sub in df.groupby("code_departement", sort=True):
    sub.to_csv(out_dir / f"{dept}.csv", index=False)
```

Each file has the **same columns** as the national file, sorted by commune
code. We get for example `75.csv` (Paris, 1 row), `13.csv`
(Bouches-du-Rhône, ~119 communes)...

> 💡 The filename is the department code (`2A.csv`, `2B.csv` for Corsica,
> `976.csv` for Mayotte), making any lookup instant.

---

## 5. Step 4 — Statistics by department

**Script:** `python scripts/04_stats_departements.py`
**Reusable module:** `src/stats.py`

We use pandas `groupby().agg()` aggregation:

```python
df.groupby("code_departement").agg(
    nb_communes=("code_commune", "count"),
    population_totale=("population", "sum"),
    surface_totale_ha=("surface_ha", "sum"),
)
```

Then we derive **density** in inhabitants/km² (careful: `surface_ha` is in
hectares, so `km² = ha / 100`).

Output: `data/final/stats_departements.csv`.

---

## 6. Why this architecture?

| Folder | Rule |
|---|---|
| `data/raw/` | **Never modified** after download. If cleaning goes wrong, delete `processed/` and re-run — no need to re-download. |
| `data/interim/` | Intermediate steps if cleaning becomes multi-stage. |
| `data/processed/` | The clean national file, ready for any use. |
| `data/final/` | Final products meant to be shared/consumed. |
| `src/` | **Reusable** code: importable functions (`from src.clean import clean_communes`). |
| `scripts/` | **Executable** code: one script = one pipeline step, numbered in order. |

**src/scripts separation**: this is the "library vs pipelines" pattern —
functions live in `src/`, orchestration (paths, order, prints) lives in
`scripts/`. Functions can then be unit-tested.

**Raw data immutability**: a founding principle of modern Data Engineering
("Data as Code" movement).

---

## 7. Verifying everything works

After the pipeline, run this check session:

```python
import pandas as pd

df = pd.read_csv("data/processed/communes_clean.csv",
                 dtype={"code_commune": str, "code_departement": str})

# 1. Consistent commune count (~35,000)
print(len(df))                       # -> 35000+

# 2. No duplicates on the key
assert df["code_commune"].is_unique

# 3. Well-formed department codes
print(sorted(df["code_departement"].unique()))

# 4. Total population ≈ 68 million
print(df["population"].sum())

# 5. Parquet read is much faster
df2 = pd.read_parquet("data/processed/communes_clean.parquet")

# 6. The split is complete: same row count
import glob
total = sum(len(pd.read_csv(f, dtype=str)) for f in glob.glob("data/final/by_departement/*.csv"))
assert total == len(df)
```

---

## 8. Common errors and fixes

| Error | Cause | Fix |
|---|---|---|
| `code_commune` loses its zeros (`"01001" -> 1001`) | Pandas inferred an integer | `dtype={"code_commune": str}` on read |
| `ValueError: Cannot convert non-finite values` | `Int64` conversion on unclean data | `errors="coerce"` BEFORE `astype("Int64")` |
| `ModuleNotFoundError: No module named 'src'` | Script run from another directory | Scripts add the project root to `sys.path` (already done here) |
| Parquet unreadable | `pyarrow` not installed | `pip install pyarrow` |
| API returns a 400 error | Requested field doesn't exist | Check the list at https://geo.api.gouv.fr/decouverte |
| Missing population | Normal: ~500 communes have no published population (merged, delegated...) | `Int64` type that accepts `NA` |

---

## 9. Going further

- **Unit tests**: `pytest` on `clean_communes` (cases: accents, codes
  with leading zeros, empty postal code list).
- **DuckDB**: SQL queries directly on Parquet files:
  `duckdb.sql("SELECT * FROM 'data/processed/*.parquet' WHERE code_departement='13'")`
- **Parameterize scripts** with `argparse` (e.g. choose a department).
- **One-command pipeline**: a `Makefile` or a `run_all.py` script.
- **Logging**: replace `print` with the `logging` module.
- **Geographic data**: request `geometry=contour` from the API and work
  with `geopandas` for maps.
