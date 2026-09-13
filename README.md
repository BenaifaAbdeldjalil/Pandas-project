# 🎓 Guide de formation — Communes de France en Python/Pandas

Objectif : apprendre en construisant, étape par étape, un pipeline qui
récupère les communes françaises, les nettoie, les découpe par
département, et sort des fichiers propres.

**Règle du jeu** : à chaque module, je t'explique le concept et te donne un
exercice précis. **Tu écris le code toi-même.** Reviens vers moi quand tu es
bloqué, quand ça plante, ou pour que je relise ce que tu as fait — je
corrigerai et t'expliquerai, mais je n'écrirai pas le projet à ta place.

Coche les cases au fur et à mesure. Ne saute pas de module : chacun
s'appuie sur le précédent.

---

## Module 0 — Mise en place de l'environnement

**Concepts** : environnement virtuel, gestion de dépendances, structure de dossiers.

1. Crée un dossier vide pour ton projet.
2. Crée un environnement virtuel Python et active-le.
## 🚀 Démarrage rapide

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # sous Windows : venv\Scripts\activate

3. Installe seulement `pandas` et `requests` pour l'instant (`pip install pandas requests`).

# 2. Installer les dépendances
pip install -r requirements.txt

4. Crée à la main cette arborescence (juste les dossiers, vides pour l'instant) :
   ```
   data/raw/
   data/processed/
   data/final/
   src/
   ```
   
New-Item -ItemType Directory -Path data
New-Item -ItemType Directory -Path src
New-Item -ItemType Directory -Path data/raw/
New-Item -ItemType Directory -Path data/processed/
New-Item -ItemType Directory -Path data/final/

5. Initialise un dépôt git (`git init`) et crée un `.gitignore` qui exclut au
   moins ton environnement virtuel.

✅ **Checkpoint** : `git status` ne doit pas te proposer d'ajouter le dossier
de ton environnement virtuel.

📚 À lire : [Python venv (doc officielle)](https://docs.python.org/3/library/venv.html)

---

## Module 1 — Aller chercher les données sur une API publique

**Concepts** : requête HTTP, JSON, `requests.get`, paramètres d'URL.

La source : **geo.api.gouv.fr**, une API publique française, gratuite, sans
clé, qui expose les communes de l'INSEE.

1. Ouvre dans ton navigateur :
   `https://geo.api.gouv.fr/communes?fields=nom,code,codeDepartement,population`
   Regarde la forme du JSON retourné : c'est une **liste d'objets**.
2. Exercice : écris un petit script Python (`test_api.py`, en dehors de
   `src/` pour l'instant, juste pour explorer) qui :
   - fait une requête GET vers cette URL avec `requests`,
   - vérifie que la requête a réussi (`response.status_code` ou `raise_for_status()`),
   - transforme la réponse en objet Python avec `.json()`,
   - affiche le nombre d'éléments récupérés et le premier élément.
3. Une fois que ça marche, écris une fonction `download_communes()` qui fait
   la même chose mais qui **sauvegarde** le résultat brut (sans le modifier)
   dans `data/raw/communes_raw.json`.

❓ **Questions à te poser** (essentielles pour bien comprendre, pas juste faire) :
- Que se passe-t-il si le serveur ne répond pas (pas de connexion) ? Comment le voir dans ton code ?
- Pourquoi est-ce important de ne jamais modifier les données dans `data/raw/` ?

✅ **Checkpoint** : le fichier `data/raw/communes_raw.json` existe et contient
environ 35 000 objets.

📚 À lire : [requests Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/), [module json (doc officielle)](https://docs.python.org/3/library/json.html)

---

## Module 2 — Charger le JSON dans un DataFrame pandas

**Concepts** : `DataFrame`, `pd.json_normalize`, exploration (`.head()`, `.info()`, `.shape`).

1. Charge le fichier `data/raw/communes_raw.json` avec le module `json`
   standard, puis transforme la liste d'objets en `DataFrame` avec
   `pd.json_normalize(...)`.
2. Explore-le : `.shape`, `.columns`, `.dtypes`, `.head()`, `.info()`.
3. Remarque une colonne bizarre : `centre.coordinates` (une liste `[lon, lat]`
   dans chaque cellule). On la traitera au module suivant.

❓ **Questions à te poser** :
- Combien de colonnes as-tu ? Correspondent-elles aux `fields` que tu as demandés à l'API ?
- Y a-t-il des colonnes avec des valeurs manquantes (`NaN`) ? Utilise `.isna().sum()`.

✅ **Checkpoint** : tu sais dire, sans hésiter, combien de lignes et de
colonnes contient ton DataFrame, et lesquelles ont des valeurs manquantes.

📚 À lire : [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)

---

## Module 3 — Nettoyer les données (le cœur du projet)

**Concepts** : renommage de colonnes, types de données, valeurs manquantes, doublons.

Fais ceci **une transformation à la fois**, en vérifiant le résultat après
chaque étape (ne code pas tout d'un coup) :

1. **Renommer les colonnes** en français clair avec `df.rename(columns={...})`
   (ex: `code` → `code_insee`, `codeDepartement` → `code_departement`).
2. **Éclater les coordonnées** : la colonne des coordonnées contient une
   liste `[longitude, latitude]`. Utilise `.apply()` avec une fonction (ou
   une lambda) pour créer deux nouvelles colonnes `longitude` et `latitude`,
   puis supprime l'ancienne colonne.
3. **Nettoyer les codes postaux** : c'est une liste de chaînes. Transforme-la
   en une seule chaîne texte, par exemple jointe avec `;`.
4. **Forcer les bons types** : `population` doit être un entier (utilise
   `pd.to_numeric(..., errors="coerce")` pour éviter un plantage si une
   valeur est bizarre), `surface` un flottant.
5. **Supprimer les lignes inexploitables** : celles sans code INSEE ou sans
   département (`.dropna(subset=[...])`). Affiche combien de lignes tu as
   supprimées.
6. **Supprimer les doublons** sur le code INSEE (`.drop_duplicates(subset=[...])`).

❓ **Questions à te poser** :
- Pourquoi utiliser `errors="coerce"` plutôt que laisser planter le script sur une valeur invalide ?
- Que se passerait-il si tu supprimais les doublons *avant* de renommer les colonnes ? Est-ce que l'ordre des opérations a de l'importance ici ?

✅ **Checkpoint** : ton DataFrame nettoyé n'a plus de valeurs manquantes sur
les colonnes clés (`code_insee`, `code_departement`), plus de doublons, et
les types de colonnes sont corrects (`df.dtypes`).

📚 À lire : [pandas — Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html)

---

## Module 4 — Organiser ton code en fonctions

**Concepts** : fonctions pures, lisibilité, fichier `.py` réutilisable.

Jusqu'ici tu as probablement tout écrit dans un seul script. C'est normal
pour explorer, mais ce n'est pas maintenable.

1. Crée `src/clean.py`.
2. Transforme **chaque transformation du Module 3** en une petite fonction
   qui prend un `DataFrame` en entrée et en renvoie un nouveau (ne modifie
   jamais le DataFrame reçu "en place" — fais `df = df.copy()` au début si besoin).
3. Crée une fonction `clean_pipeline(df)` qui appelle toutes les autres dans
   le bon ordre.

❓ **Question à te poser** :
- Pourquoi c'est utile que chaque fonction fasse *une seule chose* plutôt
  qu'une grosse fonction qui fait tout ? (Indice : pense au jour où tu
  devras corriger un bug dans une seule étape.)

✅ **Checkpoint** : tu peux appeler `clean_pipeline(df_brut)` depuis un
script séparé et obtenir le même résultat qu'au Module 3.

---

## Module 5 — Sauvegarder les données propres

**Concepts** : export CSV/Parquet, encodage, chemins de fichiers avec `pathlib`.

1. Exporte ton DataFrame nettoyé vers `data/processed/communes_clean.csv`
   avec `to_csv(..., index=False, encoding="utf-8")`.
2. Exporte-le aussi en `.parquet` (`pip install pyarrow` si besoin).

❓ **Question à te poser** :
- Ouvre les deux fichiers (CSV dans un tableur, Parquet avec
  `pd.read_parquet`). Quelle différence de taille/vitesse remarques-tu ?
  Pourquoi le Parquet garde-t-il mieux les types de données que le CSV ?

✅ **Checkpoint** : tu peux recharger le CSV avec `pd.read_csv(...)` et
retrouver exactement les mêmes colonnes et types (attention : le CSV ne
garde pas les types, il faudra peut-être les forcer à nouveau au rechargement — remarque-le).

---

## Module 6 — Découper par département (`groupby`)

**Concepts** : `groupby`, itération sur des groupes, écriture de plusieurs fichiers.

1. Utilise `df.groupby("code_departement")` pour regrouper les communes par département.
2. Itère sur les groupes (`for code_dept, group in df.groupby(...)`) et
   écris un fichier CSV par département dans `data/final/by_departement/`,
   nommé `{code_dept}.csv`.

❓ **Questions à te poser** :
- Combien de fichiers obtiens-tu ? Est-ce cohérent avec le nombre de
  départements français (100-101 avec les DOM) ?
- Que se passe-t-il pour les départements corses (`2A`, `2B`) — ton code
  les gère-t-il bien puisque ce ne sont pas des nombres ?

✅ **Checkpoint** : `ls data/final/by_departement | wc -l` te donne un nombre proche de 101.

📚 À lire : [pandas — Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html)

---

## Module 7 — Statistiques agrégées

**Concepts** : `.agg()`, colonnes calculées.

1. À partir du DataFrame nettoyé, calcule pour chaque département : nombre
   de communes, population totale, surface totale, en utilisant
   `.groupby("code_departement").agg(...)`.
2. Ajoute une colonne calculée : la densité (habitants / km²).
3. Exporte le résultat dans `data/final/stats_departements.csv`.

✅ **Checkpoint** : trie ton résultat par population décroissante — Paris
(75) doit être en tête ou très proche du sommet.

---

## Module 8 — Scripts exécutables

**Concepts** : point d'entrée `if __name__ == "__main__":`, séparation code réutilisable / code exécuté.

1. Crée un dossier `scripts/`.
2. Crée 4 fichiers numérotés (`01_download_data.py`, `02_clean_data.py`,
   `03_split_by_departement.py`, `04_stats_departements.py`) qui **importent**
   les fonctions de `src/` et les enchaînent, avec des messages clairs
   affichés (`print(...)`) pour suivre ce qui se passe.
3. Vérifie que tu peux relancer chaque script indépendamment, dans l'ordre.

✅ **Checkpoint** : en partant d'un dossier `data/` totalement vide, tu peux
reconstruire tout le pipeline en lançant les 4 scripts l'un après l'autre.

---

## Module 9 — README et documentation

**Concepts** : documenter un projet pour que quelqu'un d'autre (ou toi dans 6 mois) puisse le reprendre.

Écris un `README.md` qui explique : ce que fait le projet, comment
installer les dépendances, comment lancer le pipeline, et la structure des
dossiers.

✅ **Checkpoint** : fais lire ton README à quelqu'un (ou relis-le à froid le
lendemain) — est-ce que les instructions suffisent pour tout relancer sans
te demander d'explications supplémentaires ?

---

## Module 10 — Publier sur GitHub

**Concepts** : `git add/commit/push`, dépôt distant.

1. Vérifie ton `.gitignore` (environnement virtuel exclu, éventuellement `data/raw/` si les fichiers sont lourds).
2. `git add .`, `git commit -m "..."`, crée le dépôt sur GitHub, puis `git push`.

✅ **Checkpoint** : ton dépôt GitHub est visible en ligne, avec le README qui s'affiche correctement sur la page d'accueil.

---

## Comment utiliser ce guide avec moi

- Fais un module, code-le toi-même.
- Si tu bloques : montre-moi ton code et l'erreur exacte, je t'explique le
  problème (sans juste te donner la solution toute faite, sauf si tu me le
  demandes explicitement).
- Si tu veux, à la fin de chaque module, colle-moi ton code : je te fais une
  relecture (style, robustesse, pièges pandas classiques) avant que tu
  passes à la suite.
