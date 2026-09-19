# pandas projet

Projet pédagogique de data engineering avec Python et pandas.

L'objectif est de construire un pipeline de données sur les communes françaises à partir de l'API officielle :

https://geo.api.gouv.fr/communes

## Architecture

```text
data/
├── raw/                 # Données brutes, jamais modifiées
├── interim/             # Données intermédiaires
├── processed/           # Données nationales propres
└── final/
    └── by_departement/  # Un fichier CSV par département

src/                     # Fonctions réutilisables
scripts/                 # Scripts exécutables numérotés
docs/                    # Documentation du projet
```

## Étapes du pipeline

1. Télécharger les données brutes.
2. Nettoyer et normaliser les données.
3. Produire les fichiers CSV et Parquet.
4. Découper les communes par département.
6. Vérifier la qualité des données.

# Guide du projet

Ce document contiendra le guide complet du pipeline.

## Étapes

- TP 0 : préparation de l'environnement ;
- TP 1 : architecture du projet ;
- TP 2 : téléchargement des données ;
- TP 3 : exploration du JSON ;
- TP 4 : nettoyage ;
- TP 5 : production CSV et Parquet ;
- TP 6 : découpage par département ;
- TP 7 : statistiques ;
- TP 8 : validation ;
- TP 9 : améliorations.

## Source des données

Les données proviennent de l'API officielle du découpage administratif français :

https://geo.api.gouv.fr/communes