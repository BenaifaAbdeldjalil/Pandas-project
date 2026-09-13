# 🧭 Guide pas à pas

Ce guide t'accompagne étape par étape, sans rien brusquer. Chaque étape est
courte : fais-la, vérifie le résultat, puis passe à la suivante.

---

## Étape 0 — Préparer ton environnement

1. Assure-toi d'avoir Python 3.10+ installé :
   ```bash
   python --version
   ```
2. Place-toi dans le dossier du projet :
   ```bash
   cd commune-france-project
   ```
3. Crée un environnement virtuel (ça isole les librairies de ce projet) :
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows : venv\Scripts\activate
   ```
4. Installe les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

✅ **Vérification** : tape `pip list`, tu dois voir `pandas`, `requests`, `pyarrow`.

---

## Étape 1 — Comprendre la source de données

On utilise l'API publique **geo.api.gouv.fr**, qui expose les données
officielles de l'INSEE (communes, départements, régions, population,
surface, coordonnées géographiques). Pas besoin de clé API, pas de
limite de quota pour un usage normal.

Tu peux tester l'API toi-même dans ton navigateur :
```
https://geo.api.gouv.fr/communes?fields=nom,code,codeDepartement,population
```

---

## Étape 2 — Télécharger les données brutes

```bash
python scripts/01_download_data.py
```

Ce script :
- appelle l'API,
- récupère environ 35 000 communes,
- enregistre **sans aucune transformation** le résultat dans
  `data/raw/communes_raw.json`.

📌 **Pourquoi garder un dossier `raw/` intact ?**
Règle d'or en data science : on ne touche jamais aux données brutes. Si tu
fais une erreur dans le nettoyage, tu peux toujours repartir de zéro sans
re-télécharger.

✅ **Vérification** : ouvre `data/raw/communes_raw.json`, tu dois voir une
liste d'objets JSON avec des champs `nom`, `code`, `codeDepartement`, etc.

---

## Étape 3 — Nettoyer les données

```bash
python scripts/02_clean_data.py
```

Ce script (voir le détail dans `src/clean.py`) fait, dans l'ordre :

| Sous-étape | Ce qu'elle fait | Pourquoi |
|---|---|---|
| `rename_columns` | Renomme les colonnes en français clair | Lisibilité |
| `split_coordinates` | Sépare `[lon, lat]` en 2 colonnes | Plus facile à utiliser en pandas |
| `clean_codes_postaux` | Transforme la liste de CP en texte `"75001;75002"` | Un CSV ne gère pas bien les listes |
| `fix_dtypes` | Force les bons types (nombre, texte) | Évite les erreurs de calcul plus tard |
| `drop_incomplete_rows` | Supprime les lignes sans code INSEE/département | Données inexploitables |
| `drop_duplicates` | Supprime les doublons sur le code INSEE | Fiabilité |
| `reorder_columns` | Remet les colonnes dans un ordre logique | Lisibilité |

Résultat : `data/processed/communes_clean.csv` et `.parquet`.

✅ **Vérification** : ouvre le CSV dans un tableur, ou dans un notebook :
```python
import pandas as pd
df = pd.read_csv("data/processed/communes_clean.csv")
df.info()
df.head()
```

💡 **Pour avancer doucement** : ouvre `src/clean.py` et lis chaque fonction
une par une. Tu peux même les tester séparément dans un notebook Jupyter
avant de lancer le script complet.

---

## Étape 4 — Découper par département

```bash
python scripts/03_split_by_departement.py
```

Ce script regroupe les communes par `code_departement` avec
`df.groupby("code_departement")` et écrit un fichier CSV par groupe dans
`data/final/by_departement/`.

Exemple de fichiers générés :
```
data/final/by_departement/01.csv
data/final/by_departement/2A.csv   (Corse-du-Sud)
data/final/by_departement/75.csv   (Paris)
data/final/by_departement/971.csv  (Guadeloupe)
```

✅ **Vérification** :
```bash
ls data/final/by_departement | wc -l   # doit afficher ~101 (dont DOM)
```

---

## Étape 5 — Calculer des statistiques par département

```bash
python scripts/04_stats_departements.py
```

Génère `data/final/stats_departements.csv` avec, pour chaque département :
nombre de communes, population totale, surface totale, densité.

C'est un bon exemple pour t'entraîner à modifier le code : essaie d'ajouter
une colonne "population moyenne par commune" dans
`src/split_dept.py::compute_stats_departements`.

---

## Étape 6 — Vérifications finales avant GitHub

- [ ] `data/raw/` contient bien le JSON brut
- [ ] `data/processed/communes_clean.csv` s'ouvre sans erreur et a les bonnes colonnes
- [ ] `data/final/by_departement/` contient bien un fichier par département
- [ ] `data/final/stats_departements.csv` a des valeurs cohérentes (pas de NaN inattendu)
- [ ] Le `README.md` est à jour

---

## Étape 7 — Mettre le projet sur GitHub

```bash
cd commune-france-project
git init
git add .
git commit -m "Premier commit : pipeline communes France"
git branch -M main
git remote add origin https://github.com/TON-PSEUDO/NOM-DU-REPO.git
git push -u origin main
```

⚠️ **Astuce** : si tes fichiers de données sont volumineux (le JSON brut
peut faire plusieurs Mo), tu peux choisir de ne pas les versionner. Dans ce
cas décommente les lignes correspondantes dans `.gitignore`
(`data/raw/`, `data/interim/`), et n'oublie pas d'expliquer dans le README
qu'il faut relancer `01_download_data.py` pour régénérer les données.

---

## Pour aller plus loin (idées d'évolutions)

- Ajouter un script `05_enrichir_geo.py` qui fusionne avec d'autres jeux de
  données (ex : revenu médian par commune, data.gouv.fr).
- Ajouter des tests unitaires simples avec `pytest` sur les fonctions de
  `src/clean.py`.
- Ajouter un fichier `Makefile` pour lancer tout le pipeline en une seule
  commande (`make all`).
- Ajouter un notebook `notebooks/exploration.ipynb` pour des analyses
  visuelles (cartes avec `folium`, graphiques avec `matplotlib`).
