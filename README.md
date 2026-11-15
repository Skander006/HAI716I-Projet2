# HAI716I — Projet 2 : Dilemme du prisonnier itéré

**Université de Montpellier — M1 Informatique IASD**  
**UE :** HAI716I — Programmation Orientée Agents  
**Date :** 13–15 novembre 2026  
**Langage :** Python  
**Auteurs :** Skander SAAFI et Abdellah DORBANE

## 1. Présentation

Ce projet consiste à développer un tournoi de dilemme du prisonnier itéré inspiré des travaux de Robert Axelrod, puis à étudier les performances de différentes stratégies.

Il comprend trois étapes :

1. **Tournoi initial :** moteur de jeu et cinq stratégies du cours.
2. **Nouvelles stratégies :** ajout de GRUDGER et TIT-FOR-TWO-TATS.
3. **Modifications du tournoi :** bruit de 5 % et horizon inconnu.

Les hypothèses, expérimentations, résultats et difficultés sont détaillés dans les journaux individuels.

## 2. Organisation du projet

```text
HAI716I-Projet2/
├── engine/              # Moteur et tournoi
├── strategies_base/     # Stratégies
├── tests/               # Tests automatiques
├── journaux/            # Journaux et captures
├── main.py              # Exécution des expériences
└── README.md
```

## 3. Installation et exécution

**Prérequis :** Python 3 et Pytest (pour les tests).

Cloner le dépôt :

```bash
git clone https://github.com/Skander006/HAI716I-Projet2.git
cd HAI716I-Projet2
```

### Lancer les tournois

```bash
python main.py
```

Cette commande relance les tournois et expériences des trois étapes :

| Étape | Expériences |
|---|---|
| 1 | Tournoi initial à 5 stratégies, avec comparaison des auto-rencontres |
| 2 | Tournoi étendu à 7 stratégies et analyse des duels |
| 3 | Tournoi sans bruit, bruit de 5 %, horizon inconnu (`w=0.995`) |
| Compléments | Variations des graines et des probabilités de continuation |

### Exécuter les tests

```bash
python -m pip install pytest
python -m pytest
```

Pour exécuter un module de tests individuellement :

```bash
python -m tests.test_tournament
```

## 4. Protocole expérimental

Le protocole de référence comprend **5 parties de 200 tours** par paire de stratégies distinctes, une graine initiale fixée à **42**, sans auto-rencontres par défaut.
Matrice des gains :

| Joueur 1 / Joueur 2 | C | D |
|---|---|---|
| **C** | (3, 3) | (0, 5) |
| **D** | (5, 0) | (2, 2) |

Les stratégies implémentées sont : **ALL-D, RANDOM, TIT-FOR-TAT, TESTER, JOSS, GRUDGER et TIT-FOR-TWO-TATS**.
Les deux modifications expérimentales sont :

- **Bruit :** chaque action peut être inversée avec une probabilité de 5 %.
- **Horizon inconnu :** la partie continue après chaque tour avec une probabilité `w=0.995`, soit une durée moyenne théorique de 200 tours.

Des expériences complémentaires étudient d'autres graines et valeurs de `w`.

## 5. Journaux de bord

Chaque journal présente les contributions personnelles, les hypothèses, les tests, les résultats, les difficultés et leurs analyses.

**Skander SAAFI**

- [Journal Markdown](journaux/journal_skander_saafi/journal_skander_saafi.md)
- [Journal PDF](journaux/journal_skander_saafi/journal_skander_saafi.pdf)

**Abdellah DORBANE**

- [Journal Markdown](journaux/journal_abdellah_dorbane/journal_abdellah_dorbane.md)
- [Journal PDF](journaux/journal_abdellah_dorbane/journal_abdellah_dorbane.pdf)

Les captures d'écran sont disponibles dans les dossiers des journaux.

## 6. Conclusion

Les expériences montrent que les performances des stratégies dépendent de la population d'adversaires, des erreurs d'exécution et de la durée des interactions. Les résultats et leurs limites sont analysés dans les journaux individuels.