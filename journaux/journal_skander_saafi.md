# Journal de bord — Projet 2 : Dilemme du prisonnier itéré

**Étudiant :** Skander SAAFI  
**UE :** HAI716I - Programmation Orientée Agents  
**Langage :** Python

## 1. Organisation du travail

Nous avons réparti le développement en deux branches Git pour travailler en parallèle :

- **Ma partie (`feature/engine`) :** moteur du jeu et tournoi.
- **Mon binôme (`feature/strategies`) :** implémentation des stratégies de base.

Les deux parties seront ensuite intégrées pour réaliser les expériences.

## 2. Tournoi de base

### 2.1. Implémentation

J'ai développé le moteur du dilemme du prisonnier itéré en respectant la matrice des gains imposée et les 200 tours par partie.
Mes principaux choix techniques :

- Deux historiques indépendants, mis à jour après les deux décisions pour garantir leur simultanéité.
- Des graines pseudo-aléatoires fixes pour assurer la reproductibilité.
- Une interface commune `jouer(mes_coups, ses_coups, rng)` pour intégrer les stratégies.

J'ai ensuite implémenté le tournoi tous contre tous : chaque paire joue 5 parties de 200 tours. Les scores sont cumulés pour établir le classement.
Dans cette première version, chaque paire de stratégies distinctes joue une seule série de cinq parties. Les auto-rencontres sont exclues afin de concentrer la comparaison sur les interactions entre stratégies différentes. Ce protocole sera conservé dans les expériences suivantes pour permettre des comparaisons cohérentes.
### 2.2. Tests et difficultés

J'ai testé le moteur avec trois stratégies simples : ALL-C, ALL-D et TIT-FOR-TAT.
Les tests automatiques ont permis de vérifier la matrice des gains, les scores cumulés et le classement. Les résultats sont identiques lors de deux exécutions avec la même graine. Tous les tests ont réussi.

**Résultats des tests :**

![Résultats des tests du moteur et du tournoi](img.png)

J'ai également résolu des problèmes d'importation entre modules Python et ajouté l'attribut `nom` aux stratégies de test pour permettre leur classement.

### 2.3. Résultats et analyse des cinq stratégies


## 3. Ajout de nouvelles stratégies


## 4. Modifications du tournoi et expérimentations


## 5. Bilan final

