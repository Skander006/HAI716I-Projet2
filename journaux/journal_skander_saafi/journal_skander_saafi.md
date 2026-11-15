# Journal de bord — Projet 2 : Dilemme du prisonnier itéré

**Étudiant :** Skander SAAFI  
**UE :** HAI716I - Programmation Orientée Agents  
**Langage :** Python
**Période :** 13–15 novembre 2026

## Partie 1 - Présentation du projet

### 1.1. Introduction

Ce projet consiste à développer un tournoi de dilemme du prisonnier itéré, inspiré des travaux de Robert Axelrod, afin d'étudier les interactions entre différentes stratégies.
L'objectif est de comparer les cinq stratégies étudiées en cours, d'en introduire de nouvelles, puis d'observer comment des modifications du tournoi influencent leurs performances.
Une attention particulière sera portée aux conditions favorisant la coopération, aux réactions face aux défections et aux différences entre les résultats obtenus et ceux du tournoi historique d'Axelrod.

### 1.2. Protocole expérimental

Le tournoi repose sur le dilemme du prisonnier itéré. À chaque tour, deux joueurs choisissent simultanément de coopérer (C) ou de faire défection (D), sans connaître le choix courant de leur adversaire.
Les gains sont définis par la matrice suivante :

| | Adversaire C | Adversaire D |
|---|---|---|
| **Joueur C** | (3, 3) | (0, 5) |
| **Joueur D** | (5, 0) | (2, 2) |

Le protocole initial comprend :

- **Population :** ALL-D, RANDOM, TIT-FOR-TAT, TESTER et JOSS.
- **Durée :** 200 tours par partie.
- **Répétitions :** 5 parties par paire de stratégies.
- **Graine pseudo-aléatoire :** 42, incrémentée selon le numéro de la partie.
- **Classement :** cumul des points obtenus par chaque stratégie.

Ces paramètres reprennent le cadre du tournoi demandé. La graine fixe permet de reproduire les expériences, notamment lorsque les stratégies utilisent des décisions aléatoires.
Dans notre première implémentation, chaque paire de stratégies distinctes joue cinq parties, sans confrontation d'une stratégie contre elle-même. Nous évitons également de répéter les confrontations inversées. Ces deux choix sont distincts et peuvent influencer le classement final.
Les expériences suivantes conserveront ce protocole de référence, sauf pour les paramètres explicitement modifiés, afin de faciliter les comparaisons.

### 1.3. Organisation du travail

Le développement a été réparti sur deux branches Git pour travailler en parallèle :

- **Ma partie (`feature/engine`) :** développement du moteur du jeu, du tournoi et des tests automatiques.
- **Partie de mon binôme (`feature/strategies_base`) :** implémentation des stratégies.

Nous avons défini une interface commune `jouer(mes_coups, ses_coups, rng)` afin de faciliter l'intégration des deux parties.
Les modifications sont enregistrées par des commits Git pour conserver une trace du développement.

## Partie 2 — Développement et expérimentations

### 2.1. Étape 1 — Tournoi de base

#### 2.1.1. Hypothèses initiales

Avant d'analyser les résultats du tournoi initial, je m'attendais à ce que TIT-FOR-TAT obtienne un bon classement, notamment grâce à sa capacité à coopérer avec les stratégies coopératives tout en sanctionnant les défections. Son comportement simple et réciproque avait notamment permis d'obtenir de bons résultats dans les tournois historiques d'Axelrod.
Je pensais également que ALL-D serait performante face aux stratégies qui coopèrent fréquemment, puisqu'elle peut exploiter leur coopération. En revanche, face à des stratégies capables de riposter, ses gains risquaient d'être limités.
Concernant RANDOM, je m'attendais à des résultats irréguliers, car ses décisions ne tiennent pas compte du comportement de l'adversaire.
Enfin, je supposais que TESTER et JOSS pourraient profiter de certaines stratégies coopératives, mais que leurs défections risquaient également de provoquer des représailles et de réduire leurs scores à long terme.
Mon hypothèse principale était donc que TIT-FOR-TAT figurerait parmi les stratégies les mieux classées, sans nécessairement terminer première, puisque le résultat dépend aussi des adversaires présents et du protocole du tournoi.

#### 2.1.2. Implémentation
J'ai commencé par développer le moteur d'une partie, puis le système permettant d'organiser un tournoi entre plusieurs stratégies.
Trois choix techniques ont guidé mon implémentation :

- **Simultanéité des décisions :** chaque stratégie dispose de son propre historique et de celui de son adversaire. Les historiques sont mis à jour uniquement après les deux décisions, afin qu'aucun joueur ne puisse connaître le coup courant de l'autre.
- **Reproductibilité :** les décisions aléatoires reposent sur des générateurs initialisés avec des graines déterminées, permettant de relancer les expériences dans les mêmes conditions.
- **Extensibilité :** toutes les stratégies utilisent l'interface `jouer(mes_coups, ses_coups, rng)`, ce qui permet d'en ajouter sans modifier le fonctionnement général du moteur.

J'ai ensuite implémenté le tournoi tous contre tous. Chaque paire de stratégies distinctes joue cinq parties de 200 tours, et les scores sont cumulés pour établir un classement décroissant.
Cette séparation entre moteur, tournoi et stratégies facilite les tests et permettra d'introduire les modifications expérimentales sans reconstruire l'ensemble du programme.
Pour le tournoi initial, nous avons utilisé les cinq stratégies étudiées en cours. Le tableau suivant résume leurs règles, leurs origines et leurs comportements attendus face aux autres stratégies.

| Stratégie | Origine | Règle de fonctionnement | Forces et faiblesses attendues |
|---|---|---|---|
| **ALL-D** | Stratégie de référence étudiée en cours. | Joue toujours D, quel que soit le comportement adverse. | Exploite les stratégies coopératives, mais obtient des gains limités face aux adversaires qui ripostent systématiquement. |
| **RANDOM** | Stratégie aléatoire de référence étudiée en cours. | Choisit C ou D aléatoirement à chaque tour. | Imprévisible, mais incapable d'adapter ses décisions à l'historique adverse. |
| **TIT-FOR-TAT** | Stratégie présentée par Anatol Rapoport lors des tournois d'Axelrod. | Commence par C, puis reproduit le dernier coup de l'adversaire. | Favorise la coopération réciproque et sanctionne rapidement les défections, mais peut être entraînée dans des cycles de représailles. |
| **TESTER** | Stratégie étudiée en cours, issue des stratégies exploratoires du dilemme du prisonnier itéré. | Commence par tester l'adversaire avec une défection. Selon sa réaction, elle poursuit une exploitation périodique ou adopte un comportement de type TIT-FOR-TAT. | Peut exploiter les adversaires tolérants, mais risque de déclencher des représailles durables. |
| **JOSS** | Variante historique de TIT-FOR-TAT étudiée en cours. | Suit TIT-FOR-TAT, mais effectue occasionnellement une défection lorsque la coopération était prévue (probabilité de 10 % dans notre implémentation). | Peut obtenir un gain supplémentaire ponctuel, mais risque de perturber une coopération stable. |

Ces stratégies présentent des comportements différents : certaines privilégient systématiquement la défection, d'autres favorisent la réciprocité ou introduisent une part d'aléatoire. Cette diversité permet d'étudier l'influence de la composition du tournoi sur les performances individuelles.

#### 2.1.3. Tests et difficultés

Avant d'intégrer les cinq stratégies du cours, j'ai vérifié le moteur avec trois stratégies simples : ALL-C, ALL-D et TIT-FOR-TAT.
Les tests automatiques ont permis de contrôler :

- **La matrice des gains :** vérifier que les décisions C et D produisent les scores attendus.
- **Le cumul des scores :** vérifier que les points sont correctement additionnés sur plusieurs parties.
- **Le classement :** vérifier que les stratégies sont triées selon leur score total.
- **La répétabilité :** vérifier que deux exécutions du même scénario produisent des résultats identiques.

Tous les tests réalisés ont réussi.

**Capture d'écran des tests :**

![Résultats des tests du moteur et du tournoi](resultats_test_moteur_tournoi.png)

Lors des premiers tests, j'ai rencontré un problème d'importation entre les modules du moteur et ceux du tournoi. J'ai vérifié l'organisation des fichiers et adapté la manière d'exécuter les tests pour que Python reconnaisse correctement les modules du projet.
Un second problème concernait les stratégies fictives utilisées pour les tests : elles ne possédaient pas l'attribut `nom`, pourtant nécessaire au dictionnaire des scores. J'ai ajouté cet attribut afin de rendre les stratégies de test compatibles avec le tournoi.
Ces difficultés ont permis de clarifier le contrat entre les stratégies et le moteur. Les tests réalisés avec des stratégies simples ont validé le fonctionnement de base avant l'intégration de stratégies plus complexes.

#### 2.1.4. Résultats et analyse
**a) Classement du tournoi initial**

Après l'intégration des cinq stratégies, nous avons exécuté le tournoi selon le protocole défini précédemment : cinq parties de 200 tours pour chaque paire de stratégies distinctes, sans auto-rencontres.

Le classement obtenu est le suivant :

| Rang | Stratégie | Score total |
|---|---|---|
| 1 | ALL-D | 9536 |
| 2 | TESTER | 9022 |
| 3 | TIT-FOR-TAT | 9009 |
| 4 | JOSS | 8705 |
| 5 | RANDOM | 8324 |

**Capture d'écran du classement initial :**

![Classement initial du tournoi](classement_initial.png)

**b) Comparaison avec les hypothèses initiales**

Mon hypothèse initiale était que TIT-FOR-TAT figurerait parmi les stratégies les mieux classées grâce à sa capacité à maintenir une coopération réciproque.
Cependant, dans notre configuration sans auto-rencontres, ALL-D a obtenu le meilleur score total.
Ce résultat peut s'expliquer par la composition du tournoi : ALL-D profite des stratégies qui coopèrent suffisamment souvent, tandis que TIT-FOR-TAT peut perdre des points face aux adversaires qui provoquent des défections ou des cycles de représailles.
Le résultat ne signifie donc pas qu'ALL-D est systématiquement supérieure à TIT-FOR-TAT. Il montre plutôt que les performances d'une stratégie dépendent des adversaires rencontrés et des règles du tournoi.

**c) Influence des auto-rencontres**

Pour mieux comprendre ce résultat, nous avons comparé deux configurations :

- **Configuration A :** chaque stratégie affronte uniquement les autres stratégies.
- **Configuration B :** les confrontations d'une stratégie contre elle-même sont également autorisées.

Dans les conditions testées, nous avons observé que **ALL-D terminait première dans la configuration A**, tandis que **TIT-FOR-TAT retrouvait la première place dans la configuration B**.

| Rang | Stratégie | Score total |
|---|---|---:|
| 1 | TIT-FOR-TAT | 12 009 |
| 2 | TESTER | 11 687 |
| 3 | ALL-D | 11 536 |
| 4 | RANDOM | 10 810 |
| 5 | JOSS | 10 723 |

**Capture d'écran de la comparaison :**

![Comparaison avec et sans auto-rencontres](etape1_auto_rencontres.png)

L'ajout des auto-rencontres modifie le classement initial : TIT-FOR-TAT passe de la troisième à la première place, tandis qu'ALL-D descend de la première à la troisième.
Cette évolution s'explique notamment par les gains obtenus lors des confrontations d'une stratégie contre elle-même.
TIT-FOR-TAT coopère systématiquement avec une copie d'elle-même, ce qui lui rapporte 3 points par tour, soit 3 000 points sur cinq parties de 200 tours.
À l'inverse, ALL-D joue toujours D contre elle-même et obtient 2 points par tour, soit 2 000 points sur les cinq parties.
Ainsi, les auto-rencontres apportent 1 000 points supplémentaires à TIT-FOR-TAT par rapport à ALL-D, ce qui suffit à inverser leur position dans notre classement.
Cette expérience montre que le protocole du tournoi, et notamment l'inclusion ou non des auto-rencontres, peut influencer fortement les résultats.


**d) Comparaison avec les résultats d'Axelrod**

Dans les tournois historiques d'Axelrod, TIT-FOR-TAT s'est distinguée par ses bonnes performances, malgré sa règle très simple.
Dans notre tournoi initial sans auto-rencontres, elle ne termine pas première, contrairement au résultat historique souvent associé à cette stratégie.
Plusieurs différences peuvent expliquer cet écart : le nombre et la nature des stratégies participantes, l'absence d'auto-rencontres et les modalités de calcul des scores.
Notre comparaison montre ainsi qu'un classement ne constitue pas une propriété absolue d'une stratégie : il dépend du contexte expérimental.

**Conclusion de l'étape 1**

Cette première expérience m'a permis de vérifier le fonctionnement du moteur et de constater que les choix de protocole peuvent influencer fortement les résultats.
L'observation la plus importante est le changement de stratégie gagnante lorsque les auto-rencontres sont incluses. Elle souligne la nécessité de préciser les règles du tournoi avant de comparer les performances des stratégies.

### 2.2. Étape 2 - Ajout de nouvelles stratégies

#### 2.2.1. Hypothèses initiales

Avant d'exécuter le tournoi avec les deux nouvelles stratégies, j'ai formulé plusieurs hypothèses concernant leur comportement et leur influence sur le classement général.
L'objectif de cette deuxième expérience est d'étudier comment deux approches opposées face aux défections - la punition permanente et la tolérance - peuvent influencer les performances dans un dilemme du prisonnier itéré.

**a) Hypothèses concernant GRUDGER**

GRUDGER commence par coopérer et maintient cette coopération tant que son adversaire ne fait pas défection. Dès qu'une défection est observée, elle répond par une défection permanente, même si l'adversaire recommence à coopérer.
Je m'attends à ce que cette stratégie soit particulièrement performante face aux adversaires qui coopèrent systématiquement ou qui ne font jamais défection en premier, comme TIT-FOR-TAT. Dans ce cas, les deux stratégies peuvent maintenir une coopération mutuelle et obtenir chacune 3 points par tour.
En revanche, GRUDGER risque d'être moins performante face à RANDOM, JOSS ou TESTER. Une seule défection adverse suffit à provoquer une rupture définitive de la coopération, ce qui peut limiter les gains des deux joueurs pendant le reste de la partie.
Je suppose donc que GRUDGER obtiendra un classement relativement favorable face aux stratégies coopératives, mais que son absence de pardon constituera une faiblesse importante dans une population comportant des stratégies provocatrices ou aléatoires.

**b) Hypothèses concernant TIT-FOR-TWO-TATS**

TIT-FOR-TWO-TATS adopte un comportement plus tolérant. Elle commence par coopérer et ne fait défection que lorsque son adversaire a joué D lors des deux tours précédents.
Contrairement à TIT-FOR-TAT, qui réagit immédiatement à une défection, TIT-FOR-TWO-TATS accepte donc une défection isolée sans sanction.
Je m'attends à ce que cette tolérance favorise le maintien de la coopération face aux stratégies qui font occasionnellement défection, notamment JOSS. Elle pourrait ainsi éviter certains cycles de représailles et obtenir de meilleurs scores que TIT-FOR-TAT dans certaines confrontations.
Cependant, cette indulgence peut également être exploitée. Face à un adversaire qui alterne régulièrement coopération et défection sans jamais faire défection deux fois consécutivement, TIT-FOR-TWO-TATS risque de continuer à coopérer sans sanctionner ce comportement.
Face à ALL-D, elle devrait également subir une perte initiale avant de réagir, puisqu'elle attend deux défections consécutives avant de faire elle-même défection.
Je suppose donc que TIT-FOR-TWO-TATS sera particulièrement intéressante face aux défections occasionnelles, mais potentiellement vulnérable face aux stratégies capables d'exploiter sa tolérance.

**c) Hypothèses sur l'évolution du classement général**

L'ajout de GRUDGER et TIT-FOR-TWO-TATS modifie la composition du tournoi, qui passe de cinq à sept stratégies.
Je m'attends à ce que cette modification influence les scores et éventuellement le classement des cinq stratégies initiales, puisque chacune affrontera désormais deux adversaires supplémentaires.
GRUDGER pourrait favoriser les stratégies qui maintiennent une coopération stable, tandis que TIT-FOR-TWO-TATS pourrait offrir de nouvelles possibilités d'exploitation aux stratégies qui font défection occasionnellement.
Je ne suppose donc pas que le classement initial, dominé par ALL-D, restera nécessairement inchangé.
Mon hypothèse principale est que **la tolérance et la sévérité ne constituent pas des avantages absolus** : leur efficacité dépend du comportement des adversaires et de la fréquence des défections.

**d) Protocole de comparaison prévu**

Pour tester ces hypothèses, je conserverai les paramètres du tournoi initial :

- 200 tours par partie ;
- 5 parties par paire de stratégies ;
- graine pseudo-aléatoire initiale fixée à 42 ;
- absence d'auto-rencontres ;
- absence de répétition des confrontations inversées ;
- classement établi à partir du cumul des scores.

La seule modification sera l'ajout de GRUDGER et TIT-FOR-TWO-TATS aux cinq stratégies initiales.
Je comparerai ensuite le classement des sept stratégies avec celui du tournoi initial, en examinant particulièrement les performances de GRUDGER, TIT-FOR-TWO-TATS, TIT-FOR-TAT et ALL-D.
Cette comparaison permettra de déterminer si les observations confirment mes hypothèses et d'identifier les comportements favorisant ou limitant la coopération.

#### 2.2.2. Implémentation

Pour cette deuxième étape, nous avons ajouté deux nouvelles stratégies au tournoi initial : GRUDGER et TIT-FOR-TWO-TATS. Le tournoi passe ainsi de cinq à sept stratégies.
Notre choix permet de comparer deux comportements opposés face aux défections : une stratégie qui sanctionne définitivement la première trahison et une autre qui tolère les défections isolées.

**a) GRUDGER — Une stratégie sans pardon**

GRUDGER, implémentée par mon binôme, commence par coopérer et continue tant que son adversaire n'a jamais fait défection.
Dès qu'une défection adverse est observée, elle joue définitivement D, même si l'adversaire recommence à coopérer.
Son fonctionnement repose sur une vérification de l'historique adverse : si celui-ci contient au moins un D, la stratégie fait défection.
Cette implémentation ne nécessite aucune variable d'état supplémentaire, puisque l'historique conserve toutes les décisions précédentes.

**b) TIT-FOR-TWO-TATS — Une stratégie tolérante**

De mon côté, j'ai choisi d'implémenter TIT-FOR-TWO-TATS, une variante de TIT-FOR-TAT qui introduit davantage de tolérance.
Contrairement à TIT-FOR-TAT, qui reproduit immédiatement le dernier coup adverse, TIT-FOR-TWO-TATS ne fait défection que si l'adversaire a joué D lors des deux derniers tours consécutifs.
Son comportement repose sur trois règles :

1. Si l'adversaire a joué moins de deux coups, coopérer.
2. Si ses deux derniers coups sont D, faire défection.
3. Dans tous les autres cas, coopérer.

Cette stratégie ne conserve pas non plus d'état interne : elle utilise directement les deux derniers éléments de l'historique adverse.
L'objectif de cette implémentation est d'étudier si une tolérance supplémentaire peut préserver la coopération face aux défections occasionnelles, tout en observant les risques d'exploitation associés.

**c) Intégration des nouvelles stratégies**

Les deux stratégies respectent l'interface commune `jouer(mes_coups, ses_coups, rng)` utilisée par le moteur.
Leur intégration ne nécessite donc aucune modification du mécanisme de décision simultanée ni de la matrice des gains.
Le tournoi étendu comprend désormais :

- ALL-D ;
- RANDOM ;
- TIT-FOR-TAT ;
- TESTER ;
- JOSS ;
- GRUDGER ;
- TIT-FOR-TWO-TATS.

Nous avons conservé le protocole expérimental initial : cinq parties de 200 tours pour chaque paire de stratégies distinctes, avec une graine initiale fixée à 42 et sans auto-rencontres.
Cette continuité permet d'étudier l'effet de l'ajout des deux stratégies sans introduire simultanément d'autres modifications expérimentales.

**d) Outil d'analyse des confrontations individuelles**

Pour approfondir l'analyse, mon binôme a également ajouté une fonction `run_duels()`.
Contrairement à `run_tournament()`, qui calcule les scores cumulés et établit le classement général, cette fonction conserve les scores de chaque confrontation individuelle.
Elle retourne un dictionnaire dont les clés correspondent aux couples de noms de stratégies et dont les valeurs représentent les points obtenus par la première stratégie face à la seconde.
Les deux scores d'une confrontation entre stratégies distinctes sont enregistrés séparément, sans rejouer la partie dans l'ordre inverse.
Cette fonction nous permet d'identifier les adversaires favorables ou défavorables à chaque stratégie et d'expliquer les variations de classement à partir des résultats des duels.
Elle constitue donc un outil complémentaire pour l'analyse expérimentale de cette deuxième étape.


#### 2.2.3. Tests et difficultés

Avant d'interpréter les résultats du tournoi étendu, j'ai réalisé des tests automatiques afin de vérifier que les sept stratégies respectaient les règles de fonctionnement attendues.

**a) Vérification des stratégies déterministes**

Pour ALL-D, j'ai vérifié qu'elle faisait systématiquement défection, indépendamment de l'historique adverse.
Pour TIT-FOR-TAT, les tests ont confirmé qu'elle coopérait au premier tour, puis reproduisait le dernier coup de son adversaire.
Pour GRUDGER, j'ai vérifié qu'elle coopérait en l'absence de défection adverse et qu'une seule défection passée suffisait à provoquer une défection permanente.
Pour TIT-FOR-TWO-TATS, j'ai testé plusieurs situations représentatives :

| Historique adverse | Décision attendue | Justification |
|---|---|---|
| Aucun coup | C | Coopération initiale |
| D | C | Une seule défection est tolérée |
| C, D | C | Défection isolée |
| D, D | D | Deux défections consécutives |
| D, C | C | Retour à la coopération |
| D, D, D | D | Défections consécutives persistantes |

Ces tests permettent notamment de vérifier les conditions initiales, les réactions aux défections et le retour à la coopération.

**b) Vérification des stratégies aléatoires**

Pour RANDOM, j'ai utilisé un générateur aléatoire contrôlé afin de vérifier que la stratégie coopérait lorsque la valeur générée était inférieure à 0,5 et faisait défection dans le cas contraire.
J'ai également comparé deux séquences produites avec la même graine pour vérifier leur reproductibilité.
Pour JOSS, j'ai testé les décisions aux limites de sa probabilité de défection de 10 %, ainsi que sa réaction à une défection adverse.
Ces vérifications permettent de contrôler les règles probabilistes sans dépendre de tirages imprévisibles pendant les tests.

**c) Vérification de TESTER**

J'ai également testé le comportement de TESTER dans plusieurs situations, notamment son premier coup D, son cycle de décisions face à un adversaire coopératif et le passage à son mode de riposte.
Ces tests vérifient le comportement de l'implémentation actuelle. L'interprétation exacte de la riposte reste toutefois un choix de modélisation important, susceptible d'influencer les résultats expérimentaux.

**d) Difficulté rencontrée et correction**

Lors de la première exécution des tests de TIT-FOR-TWO-TATS, une assertion a échoué dès le premier tour.
La stratégie retournait D alors que son comportement attendu était de commencer par C.
Après vérification, j'ai identifié une erreur dans la condition traitant les historiques adverses contenant moins de deux coups : j'avais écrit `return D` au lieu de `return C`.
J'ai corrigé cette instruction, puis relancé les tests. Toutes les stratégies ont ensuite passé les vérifications prévues.
Cette difficulté a montré l'importance de tester les cas limites, notamment les premiers tours, avant d'exécuter un tournoi complet.

**e) Résultat des tests**

Les tests réalisés sur les sept stratégies ont réussi après correction.
Ils permettent de vérifier les règles de décision dans les situations étudiées, sans constituer une preuve exhaustive de l'absence de défauts.
**Capture d'écran des tests des sept stratégies :**

![Tests des sept stratégies](tests_sept_strategies.png)

#### 2.2.4. Résultats et analyse

**a) Classement du tournoi à sept stratégies**

Après l'intégration de GRUDGER et TIT-FOR-TWO-TATS, nous avons relancé le tournoi avec les sept stratégies, en conservant les paramètres de l'expérience initiale :
- 5 parties par paire de stratégies ;
- 200 tours par partie ;
- graine initiale fixée à 42 ;
- aucune auto-rencontre.

Le classement obtenu est le suivant :

| Rang | Stratégie | Score total |
|---|---|---:|
| 1 | GRUDGER | 15 493 |
| 2 | TIT-FOR-TAT | 15 009 |
| 3 | TESTER | 14 697 |
| 4 | TIT-FOR-TWO-TATS | 14 630 |
| 5 | JOSS | 13 957 |
| 6 | ALL-D | 13 581 |
| 7 | RANDOM | 12 585 |

**Capture d'écran du classement :**

![Classement du tournoi à sept stratégies](classement_etape2.png)

Le premier résultat marquant est la victoire de GRUDGER, qui termine devant TIT-FOR-TAT avec 484 points d'avance.
L'ajout des deux nouvelles stratégies modifie également le classement des stratégies initiales : ALL-D passe de la première à la sixième place, tandis que TIT-FOR-TAT passe de la troisième à la deuxième.
Ce changement montre que la performance d'une stratégie dépend non seulement de ses propres règles, mais aussi des comportements des autres stratégies présentes dans le tournoi.

**b) Analyse des confrontations individuelles avec `run_duels()`**

Pour comprendre les résultats, nous avons utilisé la fonction `run_duels()`, développée par mon binôme.
Contrairement à `run_tournament()`, qui retourne les scores cumulés, cette fonction conserve les scores obtenus contre chaque adversaire.
Elle utilise le même ordre des stratégies, les mêmes graines aléatoires et les mêmes paramètres que le tournoi général.
Cette précaution est particulièrement importante pour RANDOM et JOSS : comme le moteur attribue un générateur aléatoire distinct à chaque joueur, inverser l'ordre des stratégies peut modifier leurs décisions et donc les résultats.

**Capture d'écran des confrontations individuelles :**

![Scores des duels du tournoi à sept stratégies](duels_etape2.png)
Nous avons également vérifié que, pour chaque stratégie, la somme des scores individuels retournés par `run_duels()` correspond au score total calculé par `run_tournament()`.
Cette vérification a été effectuée avec et sans auto-rencontres.
Elle permet de contrôler la cohérence entre les résultats détaillés et le classement général, sans pour autant démontrer que toutes les règles des stratégies sont exemptes d'erreurs.

**c) Pourquoi GRUDGER termine-t-elle première ?**

GRUDGER obtient 15 493 points, soit le meilleur score du tournoi.
Ses résultats individuels permettent de comprendre cette performance :

| Adversaire | Score de GRUDGER |
|---|---:|
| ALL-D | 1 990 |
| RANDOM | 3480 |
| TIT-FOR-TAT | 3 000 |
| TESTER | 2 005 |
| JOSS | 2 018 |
| TIT-FOR-TWO-TATS | 3 000 |
| **Total** | **15 493** |

Face à TIT-FOR-TAT et TIT-FOR-TWO-TATS, GRUDGER coopère pendant les 200 tours. Aucun joueur ne déclenche de défection, ce qui produit un gain de 3 points par tour, soit 3 000 points sur les cinq parties.
Face à ALL-D, GRUDGER coopère au premier tour et perd 0 contre 5. Dès le deuxième tour, elle fait définitivement défection. Elle obtient donc 199 × 2 = 398 points par partie, soit 1 990 points au total.
Face à RANDOM, GRUDGER obtient 3 480 points. Après la première défection de RANDOM, elle adopte un comportement permanent de défection et profite des coopérations occasionnelles de son adversaire.
En revanche, face à TESTER et JOSS, une défection suffit à interrompre définitivement la coopération. GRUDGER ne pardonne jamais, même lorsque son adversaire recommence à jouer C.
Ces résultats confirment en grande partie mes hypothèses : GRUDGER est particulièrement efficace contre les stratégies coopératives, mais son absence de pardon peut limiter ses gains face à des adversaires qui provoquent des défections.
Sa première place montre que, dans cette population précise et sans erreurs d'exécution, la punition permanente peut être avantageuse.

**d) Analyse de TIT-FOR-TWO-TATS : les limites de la tolérance**

La stratégie que j'ai implémentée, TIT-FOR-TWO-TATS, termine quatrième avec 14 630 points.
Elle commence par coopérer et ne fait défection que lorsque son adversaire a joué D deux fois consécutivement.
Cette règle lui permet de maintenir la coopération avec GRUDGER et TIT-FOR-TAT, puisqu'aucune de ces stratégies ne déclenche spontanément une défection dans ces confrontations.
Cependant, les résultats révèlent une faiblesse importante face à TESTER.
TESTER obtient 3 670 points contre TIT-FOR-TWO-TATS.
Lorsque TESTER n'observe aucune riposte, elle répète un comportement comprenant une défection tous les trois tours : D, C, C, D, C, C, ...
Or, TIT-FOR-TWO-TATS ne réagit qu'à deux défections consécutives. Comme TESTER ne joue jamais deux D de suite dans ce cycle, TIT-FOR-TWO-TATS continue à coopérer.
TESTER profite alors régulièrement de cette coopération pour obtenir 5 points lorsqu'elle joue D, tandis que TIT-FOR-TWO-TATS obtient 0 point sur ces tours.
Cette confrontation illustre un compromis fondamental : une stratégie tolérante évite certaines représailles inutiles, mais peut être exploitée par un adversaire qui fait défection régulièrement sans jamais dépasser son seuil de tolérance.
Ainsi, ma stratégie fonctionne bien face à des adversaires coopératifs, mais sa règle de punition est insuffisante contre certains comportements opportunistes.

**e) Comparaison avec le tournoi initial**

Dans le tournoi à cinq stratégies, ALL-D terminait première avec 9 536 points, tandis que TIT-FOR-TAT était troisième avec 9 009 points.
Après l'ajout de GRUDGER et TIT-FOR-TWO-TATS, TIT-FOR-TAT remonte à la deuxième place, alors qu'ALL-D descend à la sixième.
L'explication principale vient des nouvelles interactions possibles.
TIT-FOR-TAT dispose désormais de deux partenaires avec lesquels elle peut maintenir une coopération stable. Contre chacune de ces stratégies, elle peut obtenir 3 000 points.
ALL-D, au contraire, ne peut exploiter GRUDGER et TIT-FOR-TWO-TATS que temporairement : toutes deux finissent par sanctionner ses défections.
ALL-D conserve toutefois la possibilité d'exploiter RANDOM. Sa baisse de classement ne signifie donc pas qu'elle a perdu tous ses adversaires favorables.
Il faut également éviter de comparer directement les scores bruts des deux tournois : avec sept stratégies, chacune affronte six adversaires au lieu de quatre.
Une comparaison plus pertinente repose sur les rangs, les confrontations individuelles et, si nécessaire, les scores moyens par adversaire.

**f) Confrontation avec mes hypothèses initiales**

Avant l'expérience, j'avais formulé plusieurs hypothèses.

**Hypothèse 1 — GRUDGER sera performante contre les stratégies coopératives.**

Cette hypothèse est confirmée. GRUDGER obtient 3 000 points contre TIT-FOR-TAT et TIT-FOR-TWO-TATS grâce à une coopération ininterrompue.

**Hypothèse 2 — GRUDGER sera pénalisée par les stratégies qui provoquent des défections.**

Cette hypothèse est partiellement confirmée. TESTER et JOSS interrompent sa coopération, mais les pertes correspondantes ne suffisent pas à l'empêcher de remporter le tournoi.

**Hypothèse 3 — TIT-FOR-TWO-TATS pourra mieux tolérer les défections isolées.**

Cette propriété est bien présente dans son comportement. Cependant, le tournoi montre que cette tolérance peut devenir une faiblesse, notamment face à TESTER, qui exploite systématiquement son absence de réaction.

**Hypothèse 4 — L'ajout de stratégies coopératives modifiera le classement initial.**

Cette hypothèse est confirmée. TIT-FOR-TAT progresse dans le classement, tandis qu'ALL-D recule fortement.
Ces observations montrent l'intérêt de formuler les hypothèses avant l'expérience : elles permettent de distinguer les résultats attendus des comportements réellement surprenants.

**g) Limites de l'expérience**

Même si GRUDGER termine première, ce résultat ne signifie pas qu'elle est universellement supérieure aux autres stratégies.
Premièrement, le tournoi ne contient que sept stratégies. Une population différente pourrait modifier le classement.
Deuxièmement, les décisions sont exécutées sans erreur. Dans ces conditions, deux stratégies coopératives peuvent maintenir leur coopération pendant toute la partie.
Troisièmement, la durée de chaque partie est fixée à 200 tours. Le classement pourrait évoluer avec d'autres durées ou d'autres règles d'arrêt.
Enfin, les stratégies probabilistes dépendent des tirages aléatoires. La graine fixe rend l'expérience reproductible, mais elle ne suffit pas à démontrer que les résultats seraient identiques avec d'autres graines.
Ces limites invitent à étudier la robustesse des stratégies plutôt qu'à considérer le classement obtenu comme une conclusion définitive.

**h) Conclusion de l'étape 2**

Cette deuxième étape met en évidence l'influence de la composition du tournoi sur les performances des stratégies.
GRUDGER remporte le tournoi grâce à sa capacité à maintenir la coopération avec les stratégies coopératives tout en sanctionnant définitivement les défections.
TIT-FOR-TWO-TATS montre qu'une plus grande tolérance peut préserver la coopération, mais aussi permettre une exploitation répétée par des stratégies opportunistes comme TESTER.
Le résultat le plus important est donc qu'aucune règle de comportement ne garantit à elle seule la victoire : les performances dépendent des interactions entre les stratégies et des conditions expérimentales.
Une question reste alors ouverte : **que se passerait-il si une coopération pouvait être transformée accidentellement en défection ?**
Dans ce cas, GRUDGER pourrait sanctionner définitivement une simple erreur, tandis que TIT-FOR-TWO-TATS pourrait bénéficier de sa tolérance.
Cette question constitue une motivation directe pour l'étape 3, dans laquelle nous étudierons l'influence de modifications du protocole expérimental.

### 2.3. Étape 3 - Modifications du tournoi

#### 2.3.1. Hypothèses initiales

Pour cette troisième étape, nous avons décidé de modifier deux paramètres du tournoi afin d'étudier la robustesse des stratégies dans des conditions différentes de celles du protocole initial.
Les deux modifications choisies sont :

- L'introduction d'un bruit de 5 % sur les actions exécutées.
- Le remplacement de la durée fixe de 200 tours par un horizon inconnu, avec une probabilité de continuation de 0,995 après chaque tour.

Ces modifications seront étudiées séparément afin de pouvoir identifier leur influence respective sur les résultats.
Voici mes prédictions pour les deux nouvelles modifications potentielles :

**a) Première modification : introduction d'un bruit de 5 %**

Dans le tournoi initial, les actions choisies par les stratégies sont toujours exécutées correctement.
Nous souhaitons maintenant introduire une probabilité de 5 % qu'une action soit inversée lors de son exécution : une coopération C peut devenir une défection D, et inversement.
Cette modification permet de simuler des erreurs de communication ou d'exécution.
Je suppose que ce bruit perturbera particulièrement les stratégies qui réagissent fortement aux défections.
GRUDGER, qui a remporté le tournoi précédent, risque de perdre son avantage. En effet, une seule défection accidentelle suffit à déclencher une punition permanente, même contre un adversaire qui souhaitait coopérer.
TIT-FOR-TAT pourrait également rencontrer des difficultés. Une défection accidentelle peut provoquer des représailles réciproques, entraînant une alternance durable entre coopération et défection.
À l'inverse, TIT-FOR-TWO-TATS pourrait mieux résister aux erreurs isolées, puisqu'elle ne sanctionne que deux défections consécutives.

**Mon hypothèse principale est donc que TIT-FOR-TWO-TATS progressera dans le classement, tandis que GRUDGER reculera.**

Je ne suppose cependant pas que TIT-FOR-TWO-TATS terminera nécessairement première : sa tolérance peut toujours être exploitée par des stratégies comme TESTER.

**b) Deuxième modification : horizon inconnu**

Dans les expériences précédentes, chaque partie durait exactement 200 tours.
Nous souhaitons maintenant introduire un horizon inconnu : après chaque tour, la partie continue avec une probabilité `w = 0,995` et s'arrête avec une probabilité de 0,005.
La durée devient donc aléatoire. Avec cette valeur de `w`, le nombre moyen de tours est de 200, ce qui permet de conserver une durée moyenne comparable à celle du tournoi initial.
Cette modification est intéressante car elle supprime la connaissance du dernier tour.
Dans un dilemme du prisonnier répété avec une durée connue, la défection peut être justifiée par un raisonnement à rebours : au dernier tour, il n'existe plus de possibilité de représailles futures.
Avec un horizon inconnu, ce raisonnement ne s'applique plus de la même manière, car les joueurs ne savent pas quand la partie se terminera.
Je suppose néanmoins que cette modification pourrait avantager ALL-D dans certaines confrontations courtes. En effet, ALL-D exploite immédiatement les stratégies qui commencent par coopérer, alors que celles-ci ont besoin de plusieurs tours pour réagir.
Cependant, les parties longues pourraient continuer à favoriser les stratégies capables de maintenir une coopération stable, comme TIT-FOR-TAT et GRUDGER.

**Mon hypothèse principale est donc que l'horizon inconnu modifiera les écarts de scores et pourrait améliorer le classement d'ALL-D, sans garantir qu'elle remporte le tournoi.**

#### 2.3.2. Implémentation

**a) Répartition du travail**

Pour cette troisième étape, nous avons réparti les deux modifications du tournoi entre les membres du binôme.
De mon côté, j'ai pris en charge l'introduction d'un bruit de 5 % sur les actions exécutées. Mon binôme s'est occupé de l'horizon inconnu, avec une probabilité de continuation de 0,995.
Les deux modifications ont été intégrées dans le moteur commun, tout en conservant la possibilité d'exécuter les expériences précédentes.

**b) Introduction du bruit dans le moteur**

J'ai ajouté un paramètre `noise`, initialisé à `0.0` par défaut, à la fonction `play_game()`.
À chaque tour, les deux stratégies choisissent d'abord leurs actions selon leurs règles habituelles.
Le moteur applique ensuite le bruit à chacune des deux actions, à l'aide de tirages pseudo-aléatoires distincts. Avec une probabilité de 5 %, une action C devient D ou une action D devient C.
Les gains sont calculés à partir des actions réellement exécutées, et les historiques sont mis à jour avec ces mêmes actions.
Cette décision est importante : une stratégie peut ainsi observer une défection accidentelle et y réagir comme s'il s'agissait d'une défection volontaire.

**c) Gestion de l'aléatoire et reproductibilité**

Pour éviter que les tirages liés au bruit ne perturbent les décisions aléatoires des stratégies, j'ai introduit un générateur pseudo-aléatoire distinct, initialisé à partir de `seed + 3`.
Les générateurs utilisés par les stratégies et par l'horizon inconnu restent séparés.
Ce choix permet de reproduire une expérience avec les mêmes paramètres et la même graine.

**d) Intégration au tournoi**

J'ai ensuite ajouté le paramètre `noise` aux fonctions `run_tournament()` et `run_duels()`.
Ces fonctions transmettent désormais la probabilité de bruit à `play_game()` pour chaque confrontation.
Le paramètre reste désactivé par défaut, ce qui garantit la compatibilité avec les expériences précédentes.
Cette architecture permet de comparer directement le tournoi initial et le tournoi bruité, sans modifier les règles des sept stratégies.

#### 2.3.3. Tests et difficultés

**a) Vérification du fonctionnement du bruit**

Après avoir intégré le paramètre `noise` dans le moteur, j'ai réalisé plusieurs tests afin de vérifier que les actions étaient correctement inversées selon la probabilité définie.
Pour isoler le comportement du bruit, j'ai utilisé deux stratégies ALL-C, qui choisissent systématiquement de coopérer.
Trois configurations ont été testées :

| Test | Paramètre | Résultat attendu | Résultat obtenu |
|---|---|---|---|
| Sans bruit | `noise=0.0` | 600 points pour chaque joueur | Test réussi |
| Bruit maximal | `noise=1.0` | 400 points pour chaque joueur | Test réussi |
| Reproductibilité | `noise=0.05`, `seed=42` | Résultats identiques sur deux exécutions | Test réussi |

**Test 1 — Absence de bruit**

Avec `noise=0.0`, les deux stratégies ALL-C coopèrent pendant les 200 tours.
Chaque joueur obtient donc 3 points par tour, soit :

`200 × 3 = 600 points`

Le test a réussi, ce qui confirme que le moteur conserve le comportement attendu lorsque le bruit est désactivé.

**Test 2 — Bruit maximal**

Avec `noise=1.0`, toutes les actions choisies sont inversées.
Les deux stratégies ALL-C choisissent C, mais leurs actions sont systématiquement transformées en D.
Chaque joueur obtient alors 2 points par tour, soit :

`200 × 2 = 400 points`

Le test a réussi, ce qui vérifie le mécanisme d'inversion des actions.

**Test 3 — Reproductibilité du bruit**

Avec `noise=0.05`, j'ai exécuté deux fois la même confrontation en conservant la graine `seed=42`.
Les deux exécutions ont produit les mêmes scores.
Ce résultat confirme que les tirages pseudo-aléatoires sont reproductibles lorsque les paramètres restent identiques.

**b) Vérification de la compatibilité avec le tournoi initial**

Après les tests unitaires, j'ai relancé le tournoi des sept stratégies avec `noise=0.0`.
Le classement obtenu était identique à celui de l'étape 2 :

| Rang | Stratégie | Score |
|---|---|---:|
| 1 | GRUDGER | 15 493 |
| 2 | TIT-FOR-TAT | 15 009 |
| 3 | TESTER | 14 697 |
| 4 | TIT-FOR-TWO-TATS | 14 630 |
| 5 | JOSS | 13 957 |
| 6 | ALL-D | 13 581 |
| 7 | RANDOM | 12 585 |

**Capture d'écran des tests :**

![Classement des strategies avec bruit de 0.0](classement_bruit_nul.png)

Cette capture d'ecran a été prise à partir du main.py
Cette vérification montre que l'ajout du paramètre `noise` n'a pas modifié les résultats du protocole de référence lorsque le bruit est désactivé.

**c) Vérification de la cohérence des résultats**

Pour analyser les confrontations individuelles, j'ai également utilisé `run_duels()` avec `noise=0.05`.
J'ai vérifié que les scores des duels correspondaient aux scores cumulés du tournoi.
Par exemple, JOSS obtient les résultats suivants :

| Adversaire | Score de JOSS |
|---|---:|
| ALL-D | 1 958 |
| RANDOM | 2 632 |
| TIT-FOR-TAT | 2 348 |
| TESTER | 2 335 |
| GRUDGER | 2 020 |
| TIT-FOR-TWO-TATS | 3 122 |
| **Total** | **14 415** |

La somme correspond exactement au score de JOSS dans le classement général.
Cette cohérence permet d'utiliser les résultats individuels pour expliquer les performances observées.

**d) Difficultés et précautions techniques**

La principale difficulté technique de cette modification était d'introduire de l'aléatoire sans perturber les mécanismes déjà présents dans le moteur.
En particulier, RANDOM et JOSS utilisent leurs propres tirages aléatoires pour choisir leurs actions.
J'ai donc utilisé un générateur distinct pour le bruit, afin de séparer les erreurs d'exécution des décisions prises par les stratégies.
Une autre précaution importante concernait l'ordre des opérations : les stratégies doivent d'abord choisir leurs actions, puis le bruit est appliqué avant le calcul des gains et la mise à jour des historiques.
Ainsi, les stratégies réagissent aux actions réellement exécutées, y compris lorsqu'elles résultent d'une erreur.

**e) Bilan des tests**

Les trois tests du bruit ont réussi, et le tournoi sans bruit reproduit les résultats précédents.
Les résultats des duels sont également cohérents avec les scores cumulés du tournoi bruité.
Ces vérifications renforcent la confiance dans l'implémentation, même si elles ne démontrent pas à elles seules que tous les comportements possibles ont été testés.

#### 2.3.4. Résultats et analyse

##### 1) Résultats et analyse de la modification du bruit

**a) Résultats du tournoi avec un bruit de 5 %**

Après avoir vérifié le fonctionnement du bruit, nous avons exécuté le tournoi avec les sept stratégies, en conservant cinq parties de 200 tours par paire, la graine initiale 42 et l'absence d'auto-rencontres.
La seule modification par rapport au tournoi de référence est l'introduction d'une probabilité de 5 % d'inversion de chaque action exécutée.
Les résultats obtenus sont les suivants :

| Stratégie | Rang sans bruit | Rang avec bruit | Score sans bruit | Score avec bruit |
|---|---:|---:|---:|---:|
| JOSS | 5 | 1 | 13 957 | 14 415 |
| ALL-D | 6 | 2 | 13 581 | 14 412 |
| GRUDGER | 1 | 3 | 15 493 | 14 361 |
| TESTER | 3 | 4 | 14 697 | 14 286 |
| TIT-FOR-TAT | 2 | 5 | 15 009 | 14 249 |
| TIT-FOR-TWO-TATS | 4 | 6 | 14 630 | 13 822 |
| RANDOM | 7 | 7 | 12 585 | 12 776 |

**Capture d'écran du classement avec et sans bruit :**

![Comparaison des classements avec et sans bruit](comparaison_bruit_5_pourcent.png)

Cette capture d'écran est prise du résultat du main.py
Le résultat le plus surprenant est la victoire de JOSS, qui termine première avec 14 415 points, devant ALL-D avec 14 412 points.
L'écart entre les deux stratégies n'est que de trois points. Ce résultat doit donc être interprété avec prudence.
GRUDGER, qui avait remporté le tournoi sans bruit, descend à la troisième place.
TIT-FOR-TAT passe de la deuxième à la cinquième place, tandis que TIT-FOR-TWO-TATS recule de la quatrième à la sixième.
Ces changements montrent qu'une probabilité d'erreur relativement faible peut modifier fortement les interactions entre les stratégies.

**b) Analyse des confrontations individuelles avec bruit**

Pour comprendre ces résultats, nous avons utilisé `run_duels()` avec `noise=0.05`.

**Capture d'écran des duels avec bruit :**

![Duels avec un bruit de 5%](duels_bruit_5_pourcent.png)

Les scores individuels permettent d'expliquer plusieurs changements de classement.
**Pourquoi GRUDGER perd-elle sa première place ?**

Sans bruit, GRUDGER obtenait 3 000 points contre TIT-FOR-TAT et 3 000 points contre TIT-FOR-TWO-TATS.
Avec bruit, ses résultats deviennent :

| Adversaire | Sans bruit | Avec bruit | Variation |
|---|---:|---:|---:|
| TIT-FOR-TAT | 3 000 | 2 252 | -748 |
| TIT-FOR-TWO-TATS | 3 000 | 2 401 | -599 |

Ces diminutions s'expliquent par la sensibilité de GRUDGER aux défections.
Dans le tournoi sans bruit, ces confrontations pouvaient maintenir une coopération permanente.
Avec bruit, une coopération peut être accidentellement transformée en défection. Dès qu'une telle défection est observée, GRUDGER décide de ne plus coopérer.
Une erreur ponctuelle peut donc provoquer une rupture durable de la coopération.
Cela explique pourquoi GRUDGER perd une partie de son avantage initial.

**Pourquoi JOSS termine-t-elle première ?**

JOSS obtient notamment :

- 3122 points contre TIT-FOR-TWO-TATS ;
- 2632 points contre RANDOM ;
- 2348 points contre TIT-FOR-TAT ;
- 2335 points contre TESTER.

Ces confrontations contribuent à son score total de 14 415 points.
JOSS introduit déjà des défections occasionnelles dans son comportement, puisqu'elle suit TIT-FOR-TAT tout en pouvant faire défection spontanément.
Ses résultats montrent que cette stratégie reste compétitive lorsque des erreurs d'exécution sont ajoutées.
Cependant, sa première place avec la graine 42 ne suffit pas, à elle seule, à démontrer une supériorité générale.

**Pourquoi ALL-D progresse-t-elle ?**

ALL-D passe de la sixième à la deuxième place, avec une augmentation de 831 points.
Cette stratégie ne cherche jamais volontairement à maintenir une coopération.
Le bruit perturbe donc moins une relation coopérative qu'ALL-D n'essaie pas d'établir.
De plus, les erreurs peuvent provoquer des défections accidentelles chez les stratégies coopératives et déclencher des représailles qui réduisent leurs gains.
ALL-D profite ainsi d'un contexte dans lequel la coopération devient plus difficile à maintenir.
Il faut néanmoins rappeler que le bruit peut également inverser ses propres défections en coopérations : ALL-D n'est donc pas totalement insensible aux erreurs d'exécution.

**Pourquoi TIT-FOR-TWO-TATS recule-t-elle ?**

Mon hypothèse initiale était que TIT-FOR-TWO-TATS résisterait mieux au bruit grâce à sa tolérance aux défections isolées.
Pourtant, elle passe de la quatrième à la sixième place.
Face à GRUDGER, elle obtient seulement 1941 points avec bruit, contre 3000 sans bruit.
La tolérance de TIT-FOR-TWO-TATS ne suffit donc pas à préserver une coopération durable lorsque son adversaire applique une punition permanente.
Elle reste également vulnérable aux stratégies capables d'exploiter sa coopération.
Cette observation contredit mon hypothèse d'une progression de TIT-FOR-TWO-TATS au classement général.

**c) Expérience complémentaire : influence de la graine aléatoire**

Pour vérifier si la victoire de JOSS dépendait uniquement de la graine 42, nous avons répété le tournoi bruité avec dix graines différentes, de 0 à 9.
Les résultats montrent que :

- JOSS termine première avec neuf graines sur dix.
- GRUDGER termine première avec la graine 9.
- ALL-D reste troisième dans ces dix expériences.
- RANDOM termine systématiquement dernière.

Cette expérience apporte une information importante : la victoire de JOSS n'est pas limitée à la seule graine 42.
Cependant, les classements varient légèrement selon les tirages aléatoires, et ces dix graines ne permettent pas de garantir que JOSS serait toujours première.
Nous pouvons donc conclure que JOSS présente de bonnes performances dans les conditions testées, tout en conservant une certaine prudence quant à la généralisation du résultat.

##### 2) Résultats et analyse de la modification de l'horizon inconnu

**a) Résultats du tournoi avec horizon inconnu**

La deuxième modification, implémentée par mon binôme, consiste à remplacer la durée fixe de 200 tours par une probabilité de continuation après chaque tour.
Nous avons utilisé `w = 0.995`, ce qui correspond à une probabilité d'arrêt de 0,005 après chaque tour.
La durée moyenne théorique d'une partie est alors de 200 tours.
Le classement obtenu avec la graine 42 est :

| Rang | Stratégie | Score |
|---|---|---:|
| 1 | GRUDGER | 27 278 |
| 2 | TIT-FOR-TAT | 26 442 |
| 3 | TESTER | 25 894 |
| 4 | TIT-FOR-TWO-TATS | 25 813 |
| 5 | JOSS | 24 423 |
| 6 | ALL-D | 23 904 |
| 7 | RANDOM | 22 183 |

**Capture d'écran du tournoi avec horizon inconnu :**
![Classement avec horizon inconnu](classement_horizon_inconnu.png)

Le classement est identique à celui du tournoi de référence à sept stratégies.
GRUDGER conserve sa première place, suivie de TIT-FOR-TAT et TESTER.
Notre hypothèse selon laquelle l'horizon inconnu pourrait améliorer le classement d'ALL-D n'est donc pas confirmée pour `w = 0.995`.
Les scores bruts sont néanmoins plus élevés que dans le tournoi fixe.
Cela peut s'expliquer par les durées effectivement obtenues lors des tirages aléatoires. Même si la durée moyenne théorique est de 200 tours, les parties simulées peuvent être beaucoup plus courtes ou plus longues.
Il serait donc incorrect de comparer directement ces scores bruts à ceux du tournoi fixe sans tenir compte du nombre réel de tours joués.

**b) Expérience complémentaire : influence de la probabilité de continuation**

Pour approfondir l'analyse, nous avons fait varier la probabilité de continuation en exécutant 200 parties par paire de stratégies.

Les résultats sont les suivants :

| Probabilité de continuation | Durée moyenne théorique | Première stratégie | Rang d'ALL-D |
|---|---:|---|---:|
| 0,995 | 200 tours | GRUDGER | 6 |
| 0,9 | 10 tours | GRUDGER | 3 |
| 0,8 | 5 tours | ALL-D | 1 |
| 0,5 | 2 tours | ALL-D | 1 |

Cette expérience révèle une tendance importante.
Lorsque la probabilité de continuation est élevée, les parties sont généralement longues. Les stratégies capables de maintenir une coopération stable, comme GRUDGER et TIT-FOR-TAT, conservent de bonnes performances.
Lorsque la probabilité de continuation diminue, les parties deviennent plus courtes.
Dans ces conditions, ALL-D devient plus compétitive, car elle peut exploiter immédiatement les adversaires qui commencent par coopérer.
Les stratégies coopératives disposent alors de moins de tours pour compenser leurs pertes initiales ou établir une coopération durable.
ALL-D atteint ainsi la première place pour `w = 0.8` et `w = 0.5`.
Cette expérience confirme que la durée attendue des interactions influence fortement les stratégies favorisées par le tournoi.
Elle nuance également notre hypothèse initiale : l'horizon inconnu ne favorise pas nécessairement ALL-D lorsque la durée moyenne reste longue, mais les horizons très courts peuvent lui être favorables.

**c) Vérification avec d'autres graines**

Nous avons également répété le tournoi avec `w = 0.995` en utilisant les graines 0, 100 et 1000.
Le classement est resté identique lors des trois expériences :
GRUDGER > TIT-FOR-TAT > TESTER > TIT-FOR-TWO-TATS > JOSS > ALL-D > RANDOM.
Cette stabilité suggère que, pour les conditions testées, le classement est relativement robuste aux graines choisies.
Cependant, trois graines ne suffisent pas à établir une propriété générale. Des répétitions supplémentaires permettraient de mieux quantifier la variabilité des résultats.

##### 3) Comparaison avec les hypothèses initiales

Les deux modifications permettent maintenant de confronter nos prédictions aux observations.

| Hypothèse | Observation | Conclusion |
|---|---|---|
| GRUDGER sera pénalisée par le bruit | Elle passe de la 1re à la 3e place | Confirmée |
| TIT-FOR-TWO-TATS progressera grâce à sa tolérance | Elle passe de la 4e à la 6e place | Non confirmée |
| Le bruit perturbera la coopération | Les scores et les classements changent sensiblement | Confirmée dans les expériences |
| L'horizon inconnu pourrait favoriser ALL-D | ALL-D reste 6e avec `w = 0.995` | Non confirmée pour cette valeur |
| Les horizons courts favoriseront la défection | ALL-D termine première avec `w = 0.8` et `w = 0.5` | Confirmée dans les expériences complémentaires |

Ces résultats montrent l'importance de distinguer les hypothèses initiales des observations expérimentales.
Certaines prédictions ont été confirmées, tandis que d'autres ont été contredites par les résultats.
Les expériences complémentaires ont également permis d'affiner notre interprétation, notamment concernant la durée attendue des interactions.

**Conclusion de l'étape 3**

Cette troisième étape montre que les performances des stratégies dépendent fortement des conditions d'exécution du tournoi.
L'introduction d'un bruit de 5 % modifie profondément le classement. GRUDGER perd sa première place, tandis que JOSS et ALL-D deviennent particulièrement compétitives.
Cette expérience révèle les limites des stratégies qui réagissent fortement aux défections accidentelles, mais aussi le fait que la tolérance ne garantit pas systématiquement de meilleures performances.
L'horizon inconnu produit des résultats différents. Avec une probabilité de continuation de 0,995, le classement reste identique à celui du tournoi de référence.
En revanche, lorsque les parties deviennent plus courtes, ALL-D progresse jusqu'à prendre la première place.
Ces observations mettent en évidence deux facteurs importants : la fiabilité des actions exécutées et la durée attendue des interactions.
Elles confirment qu'aucune stratégie ne peut être considérée comme universellement supérieure. Son efficacité dépend de la population d'adversaires, du niveau de bruit et des conditions dans lesquelles les interactions se déroulent.

## Partie 3 — Bilan final

### 3.1. Difficultés rencontrées et solutions apportées

Au cours de ce projet, j'ai rencontré plusieurs difficultés liées à la conception du moteur de jeu, à l'implémentation des stratégies et à l'interprétation des résultats expérimentaux.
Ces difficultés m'ont permis de mieux comprendre l'importance des tests, de la reproductibilité et de la rigueur dans la conception d'un système multi-agent.

**a) Garantir la simultanéité des décisions**

L'une des premières difficultés concernait le fonctionnement du moteur du dilemme du prisonnier itéré.
Les deux joueurs doivent choisir leurs actions simultanément, sans connaître la décision actuelle de leur adversaire.
Il fallait donc éviter qu'une stratégie puisse accéder au coup choisi par l'autre joueur pendant le même tour.

Pour résoudre ce problème, j'ai organisé le moteur en trois étapes :

1. Chaque stratégie choisit son action à partir des historiques des tours précédents.
2. Le moteur calcule les gains des deux joueurs.
3. Les historiques sont mis à jour avec les actions exécutées.

Cette organisation garantit que les deux décisions sont prises à partir des mêmes informations temporelles.

**b) Assurer la cohérence entre le tournoi et les duels**

Pour comprendre les classements, nous avons ajouté une fonction `run_duels()` permettant d'obtenir les scores de chaque confrontation.
Une difficulté importante était de garantir que les scores individuels correspondent exactement aux scores cumulés par `run_tournament()`.
En effet, certaines stratégies utilisent des tirages pseudo-aléatoires, et l'ordre des joueurs peut influencer les résultats obtenus avec une graine donnée.
Nous avons donc conservé le même ordre des confrontations et les mêmes graines dans les deux fonctions.
Nous avons ensuite vérifié que la somme des scores individuels de chaque stratégie correspondait à son score dans le tournoi.
Par exemple, avec un bruit de 5 %, la somme des duels de JOSS donne exactement 14 415 points, soit son score au classement général.
Cette vérification nous a permis de fiabiliser nos analyses.

**c) Introduire le bruit sans perturber le moteur existant**

Lors de la troisième étape, ma principale difficulté technique était d'introduire une probabilité d'erreur de 5 % tout en préservant le fonctionnement des stratégies et des expériences précédentes.
J'ai choisi d'utiliser un générateur pseudo-aléatoire distinct pour le bruit, afin de ne pas modifier les tirages utilisés par les stratégies RANDOM et JOSS ou par l'horizon inconnu.
J'ai également veillé à appliquer le bruit après le choix des actions, mais avant le calcul des gains et la mise à jour des historiques.

Pour vérifier cette modification, j'ai testé trois situations :

- Un bruit nul (`noise=0.0`), qui conserve les actions choisies.
- Un bruit maximal (`noise=1.0`), qui inverse systématiquement les actions.
- Un bruit de 5 % avec une graine fixe, pour vérifier la reproductibilité.

Les trois tests ont réussi.
J'ai ensuite relancé le tournoi sans bruit et retrouvé exactement les résultats de l'étape 2, ce qui a confirmé que la modification n'avait pas perturbé le protocole initial.

**d) Comprendre des résultats contraires à mes hypothèses**

Une dernière difficulté était liée à l'interprétation des résultats.
Avant l'expérience avec bruit, je pensais que TIT-FOR-TWO-TATS progresserait grâce à sa tolérance aux défections isolées.
Pourtant, elle est passée de la quatrième à la sixième place.
À l'inverse, JOSS est passée de la cinquième à la première place.
J'ai donc analysé les duels individuels pour comprendre ces résultats plutôt que de conserver mon hypothèse initiale.
J'ai notamment observé que TIT-FOR-TWO-TATS n'obtenait plus que 1 941 points contre GRUDGER, contre 3 000 sans bruit.
Cette observation m'a montré que la tolérance aux erreurs ne suffit pas toujours à maintenir la coopération, notamment face à une stratégie qui sanctionne définitivement une défection.
J'ai également constaté que JOSS ne devançait ALL-D que de trois points avec la graine 42.
Pour éviter de tirer une conclusion trop générale, nous avons réalisé des expériences complémentaires avec dix graines différentes.
JOSS a terminé première dans neuf de ces dix expériences.
Cette démarche m'a appris à considérer une hypothèse comme une proposition à tester, et non comme une conclusion à défendre à tout prix.

**Bilan**

Ces difficultés ont été importantes dans ma progression pendant le projet.
Elles m'ont appris à vérifier les comportements des agents avec des tests ciblés, à contrôler les sources d'aléatoire et à analyser les résultats à partir de données expérimentales.
J'ai surtout compris qu'obtenir un classement ne suffit pas : il faut également être capable d'expliquer les mécanismes qui produisent les résultats et de reconnaître les limites de ses conclusions.

### 3.2. Ce que j'ai appris

Ce projet m'a permis de mieux comprendre les interactions entre agents autonomes et les mécanismes qui favorisent la coopération dans le dilemme du prisonnier itéré.

**a) L'importance des adversaires**

Au début, je pensais qu'une stratégie comme ALL-D, qui cherche à maximiser ses gains immédiats, serait particulièrement efficace.
Elle a effectivement remporté le premier tournoi. Cependant, après l'ajout de GRUDGER et TIT-FOR-TWO-TATS, elle est descendue à la sixième place.
J'ai compris que les performances d'une stratégie dépendent fortement des adversaires présents. Une stratégie gagnante dans une population peut devenir beaucoup moins efficace dans une autre.

**b) La coopération et le pardon**

La comparaison entre GRUDGER et TIT-FOR-TWO-TATS m'a montré que la coopération peut produire de meilleurs gains à long terme que la défection systématique.
Sans bruit, GRUDGER remporte le tournoi grâce à sa capacité à coopérer durablement avec certaines stratégies.
Avec un bruit de 5 %, elle perd sa première place, car une simple erreur peut déclencher une punition permanente.
Je pensais que TIT-FOR-TWO-TATS profiterait de sa tolérance aux défections isolées, mais elle a finalement reculé au classement. J'ai compris que pardonner ne suffit pas toujours : le comportement de l'adversaire compte également.

**c) L'influence du bruit et de l'horizon inconnu**

L'introduction d'un bruit de 5 % a profondément modifié le classement, avec JOSS passant de la cinquième à la première place.
Cela m'a montré qu'une petite probabilité d'erreur peut avoir des conséquences importantes sur les interactions entre agents.
L'expérience avec horizon inconnu m'a également appris que la durée attendue des interactions influence la coopération. Lorsque les parties deviennent très courtes, ALL-D devient plus compétitive et finit même première pour certaines probabilités de continuation.

**d) L'importance de la démarche expérimentale**

Enfin, j'ai appris qu'il ne suffit pas d'obtenir un classement : il faut comprendre et expliquer les résultats.
L'utilisation de graines fixes, des tests unitaires et l'analyse des duels nous ont permis de vérifier nos implémentations et de confronter nos hypothèses aux observations.
Les expériences avec plusieurs graines m'ont également montré l'importance de la reproductibilité.

**Bilan personnel**

Ce que je retiens principalement, c'est qu'aucune stratégie n'est universellement gagnante dans nos expériences. Ses performances dépendent de la population, des erreurs et de la durée des interactions.
Ce projet m'a surtout appris à raisonner de manière expérimentale : formuler des hypothèses, les tester, accepter les résultats inattendus et chercher à les expliquer.

### 3.3. Bilan de ma contribution personnelle

Dans ce projet, nous avons travaillé en binôme avec Abdellah DORBANE, en nous répartissant les tâches tout en conservant un dépôt Git commun.

**a) Développement du moteur et du tournoi**

Ma principale contribution a été la conception et l'implémentation du moteur de jeu en Python.
J'ai développé la gestion des actions, le calcul des gains, les historiques des joueurs et le déroulement des parties. J'ai également implémenté le tournoi permettant à chaque stratégie d'affronter les autres et de calculer un classement général.
J'ai veillé à rendre les expériences reproductibles grâce à l'utilisation de graines pseudo-aléatoires fixes.

**b) Implémentation de TIT-FOR-TWO-TATS**

Pour la deuxième étape, j'ai choisi et développé la stratégie TIT-FOR-TWO-TATS, qui ne riposte qu'après deux défections consécutives de son adversaire.
J'ai testé son comportement et corrigé une erreur concernant son premier coup.
Cette contribution m'a permis d'étudier les avantages et les limites d'une stratégie plus tolérante que TIT-FOR-TAT.

**c) Introduction du bruit de 5 %**

Pour la troisième étape, j'ai été responsable de l'implémentation du bruit.
J'ai ajouté la possibilité d'inverser aléatoirement les actions exécutées, en utilisant un générateur pseudo-aléatoire indépendant.
J'ai ensuite réalisé plusieurs tests pour vérifier le fonctionnement de cette modification, puis analysé son influence sur le classement et les confrontations individuelles.

**d) Collaboration et organisation**

Abdellah s'est principalement occupé des cinq stratégies initiales, de GRUDGER, de la fonction d'analyse des duels et de l'horizon inconnu.
Nous avons régulièrement intégré nos modifications dans le dépôt commun et vérifié leur compatibilité.
Cette organisation m'a appris à concevoir des composants indépendants, à respecter une interface commune et à collaborer efficacement sur un projet informatique.

**Bilan**

Je considère que ma contribution principale a été de construire une base technique fiable et extensible, permettant d'expérimenter différentes stratégies et de modifier les conditions du tournoi sans réécrire l'ensemble du programme.
Ce projet m'a permis de progresser à la fois en programmation Python, en conception logicielle, en expérimentation et en travail collaboratif.

### 3.4. Limites et améliorations possibles

Même si notre programme fonctionne et que les expériences ont donné des résultats intéressants, notre travail présente certaines limites.

**a) Une population de stratégies limitée**

Notre tournoi comporte seulement sept stratégies. Les classements dépendent donc fortement de cette population, comme nous l'avons constaté entre les étapes 1 et 2.
Une amélioration serait d'ajouter d'autres stratégies, notamment PAVLOV ou SOFT MAJORITY, afin d'étudier leur comportement face aux stratégies déjà présentes.

**b) Un nombre limité de parties**

Notre protocole principal utilise cinq parties par paire de stratégies. Ce nombre reste faible pour des expériences comportant de l'aléatoire.
Nous avons effectué des tests avec plusieurs graines, mais il serait intéressant d'augmenter le nombre de répétitions et de calculer des moyennes ainsi que des écarts-types pour mieux évaluer la stabilité des résultats.

**c) Des paramètres expérimentaux à approfondir**

Nous avons principalement étudié un bruit de 5 % et un horizon inconnu avec une probabilité de continuation de 0,995.
Nous pourrions tester plusieurs niveaux de bruit (1 %, 5 %, 10 %, 20 %) afin d'observer à partir de quel seuil les stratégies coopératives deviennent moins performantes.
Il serait également intéressant de combiner le bruit et l'horizon inconnu pour étudier les stratégies dans des conditions plus complexes.

**d) Des comportements à analyser plus précisément**

Notre programme calcule les scores et les classements, mais il pourrait également enregistrer des indicateurs supplémentaires : taux de coopération, nombre de défections, durée des parties et évolution des scores au fil des tours.
Ces informations permettraient de mieux comprendre les mécanismes à l'origine des résultats, notamment les cycles de représailles entre stratégies.

**Bilan**

Si je devais poursuivre ce projet, ma priorité serait d'enrichir les analyses expérimentales plutôt que de simplement ajouter de nouvelles stratégies.
Je chercherais notamment à mesurer la robustesse des résultats face à différents paramètres et à mieux comprendre les comportements collectifs qui émergent des interactions entre agents.