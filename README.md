# 🇫🇷 French Communes — Data Pipeline

Project for fetching, cleaning and processing data on French communes
(official source: [geo.api.gouv.fr](https://geo.api.gouv.fr), based on the
INSEE Code Officiel Géographique).

The pipeline downloads raw data, cleans it, enriches it, then generates:
- a clean national file (CSV + Parquet)
- **one CSV file per department**
- aggregate statistics by department

## 📁 Project architecture

```
commune-france-project/
├── data/
│   ├── raw/                 # Raw data as downloaded (never modified)
│   ├── interim/             # Intermediate cleaning steps
│   ├── processed/           # Clean, ready-to-use data (national file)
│   └── final/
│       └── by_departement/  # One CSV per department (e.g. 75.csv, 13.csv...)
├── src/                     # Reusable source code (functions)
│   ├── download.py          # Download from the API
│   ├── clean.py             # Cleaning functions
│   ├── split_dept.py        # Department splitting
│   └── stats.py             # Aggregate statistics
├── scripts/                 # Executable scripts, one per step
│   ├── 01_download_data.py
│   ├── 02_clean_data.py
│   ├── 03_split_by_departement.py
│   └── 04_stats_departements.py
├── docs/
│   └── GUIDE.md             # Detailed step-by-step guide (read this first!)
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Quick start

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

python scripts/01_download_data.py
python scripts/02_clean_data.py
python scripts/03_split_by_departement.py
python scripts/04_stats_departements.py
```

👉 For a detailed explanation of each step, **read `docs/GUIDE.md`**.

## 📊 Produced data

| File | Contents |
|---|---|
| `data/raw/communes_raw.json` | Raw API response |
| `data/processed/communes_clean.csv` | All communes, cleaned |
| `data/processed/communes_clean.parquet` | Same, Parquet format (faster) |
| `data/final/by_departement/{code}.csv` | One file per department |
| `data/final/stats_departements.csv` | Commune count, population, surface per department |

## 📄 Data licence

Data comes from the `geo.api.gouv.fr` API, itself based on public data
from INSEE and IGN (open licence / Etalab).
