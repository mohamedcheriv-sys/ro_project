# Projet de Recherche Opérationnelle 2026

## Réalisé par

| Numéro | Nom |
|---|---|
| C25936 | MOHAMED CHERIV |
| C30620 | MOHAMEDEN ELBEDEWI |

## Objectif

Ce dépôt contient un mini-projet de Recherche Opérationnelle en français. Il traite quatre applications :

1. Routage des camions d'eau dans les quartiers périphériques ;
2. Affectation des étudiants aux projets ;
3. Dimensionnement de stock par le modèle EOQ ;
4. Méthode du simplexe.

Le simplexe a été ajouté pour renforcer la partie fondamentale de programmation linéaire.

## Outils recommandés utilisés

Conformément aux consignes, le projet utilise du code Python et un outil recommandé : **NetworkX**.

- **NetworkX** : représentation du réseau de distribution d'eau sous forme de graphe pondéré ;
- **NumPy** : calculs numériques ;
- **Matplotlib** : génération des figures ;
- **Python standard** : lecture des données CSV, génération des résultats et méthode du simplexe.

Pyomo, PuLP ou OR-Tools peuvent être utilisés comme extensions pour des instances plus grandes. Dans cette version, NetworkX est retenu comme outil recommandé principal car il correspond directement au sujet de routage.

## Structure

```text
.
├── rapport.tex
├── presentation.tex
├── rapport.pdf
├── presentation.pdf
├── requirements.txt
├── data/
├── src/
├── results/
└── figures/
```

## Exécution du code

```bash
pip install -r requirements.txt
python src/run_all.py
```

Les résultats sont générés dans le dossier `results/` et les figures dans `figures/`.

## Compilation Overleaf

Importer le fichier ZIP dans Overleaf, puis compiler :

- `rapport.tex` pour le rapport ;
- `presentation.tex` pour la présentation.

## Remarque

Les noms et numéros des étudiants sont déjà ajoutés dans `rapport.tex`, `presentation.tex` et ce README.
