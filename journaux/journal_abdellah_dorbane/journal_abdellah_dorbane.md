# Journal de bord — Abdellah DORBANE

HAI716I, Projet 2 (partie 1) : tournoi de dilemme du prisonnier itéré.
Binôme : Skander SAAFI. Code commun, un journal chacun. Langage : Python.

---

## 1. Protocole

Ce tableau est complété au fur et à mesure du projet.

| Paramètre | Valeur | Raison |
|---|---|---|
| Gains | CC = 3/3, CD = 0/5, DC = 5/0, DD = 2/2 | matrice du cours |
| Tours par partie | 200 | format d'Axelrod |
| Parties par paire | 5 | format d'Axelrod |
| Graine | fixée dans le moteur (42) | résultats rejouables à l'identique |
| Match contre soi-même | non par défaut, option `self_play` dans le moteur | Axelrod l'incluait : effet mesuré en partie 4 |
| Population de l'étape 1 | ALL-D, RANDOM, TIT-FOR-TAT, TESTER, JOSS | imposée par l'énoncé |
| Ma nouvelle stratégie (étape 2) | GRUDGER | voir partie 5 |
| Stratégie de Skander (étape 2) | TIT-FOR-TWO-TATS | voir partie 5 |
| Modifications (étape 3) | bruit 5 % ; horizon inconnu, w = 0,995 | voir partie 6 |

---

## 2. Le point de départ (13/11)

Le sujet part du tournoi d'Axelrod vu au cours 4 : chaque stratégie affronte toutes les autres, 5 parties de 200 tours, et le meilleur score total gagne. En 1980, c'est TIT-FOR-TAT, la stratégie la plus simple, qui l'a emporté. Notre travail : reconstruire ce tournoi, voir si on retrouve ce résultat, puis le modifier.

Avec Skander, nous nous sommes réparti le travail : lui construit le moteur et le tournoi, moi j'écris les stratégies. Chacun travaille sur sa branche Git.

Pour que nos deux parties s'emboîtent, nous nous sommes d'abord mis d'accord sur une seule chose : la façon dont le moteur appelle une stratégie. Chaque stratégie a un nom et une méthode `jouer(mes_coups, ses_coups, rng)` qui renvoie C ou D. Le `rng`, c'est le hasard fourni par le moteur avec une graine fixe : c'est ce qui permet de relancer le tournoi et d'obtenir exactement le même résultat, comme le demande l'énoncé.

À partir de là, j'ai écrit les stratégies une par une, avec un commit pour chacune.

---

## 3. Étape 1 — Les cinq stratégies du cours (13/11)

### 3.1. ALL-D, la trahison systématique

J'ai commencé par la plus simple : ALL-D joue toujours D. Le cours la présente comme la stratégie « rationnelle » : au dernier tour, trahir rapporte plus ; donc à l'avant-dernier aussi ; et en remontant ainsi, on trahit dès le premier tour.

Sur le papier, elle devrait écraser RANDOM, qui coopère une fois sur deux sans jamais se venger : chaque C de RANDOM lui rapporte 5 points. Mais face à TIT-FOR-TAT, elle ne gagne que le premier tour : ensuite les deux jouent D et ALL-D tombe à 2 points par tour, alors que deux stratégies qui coopèrent en gagnent 3.

**Mon avis :** ALL-D gagne tous ses duels ou fait match nul, mais je pense que ce n'est pas suffisant pour gagner un tournoi. Ce qui compte, c'est le total des points, et ALL-D se prive des 3 points par tour de la coopération. Elle ne peut finir en tête que si la population contient beaucoup de stratégies faciles à exploiter.

### 3.2. RANDOM, le témoin

RANDOM joue C ou D à pile ou face. Elle ne cherche pas à gagner : elle sert de référence. Une stratégie qui fait moins bien que le hasard a clairement un problème.

Elle n'a pas d'adversaire favorable particulier, et elle devrait souffrir face à ALL-D, qui profite de chacun de ses C.

**Mon avis :** comme elle ne réagit à rien, elle ne peut ni punir ni être récompensée. Je m'attends à la voir en bas du classement.

### 3.3. TIT-FOR-TAT, la gagnante de 1980

TIT-FOR-TAT commence par C, puis recopie le dernier coup de l'adversaire. Gentille au départ, elle punit une trahison au tour suivant, et pardonne dès que l'adversaire revient à C.

Contre les stratégies gentilles, et contre elle-même, elle coopère tout le temps : 3 points par tour. En revanche, elle ne gagne jamais un duel : contre ALL-D, elle perd le premier tour et ne rattrape jamais. Toute sa force vient de l'ensemble des rencontres, pas d'un duel en particulier. Contre JOSS, je m'attends à des représailles en écho (voir 3.5).

**Mon avis :** sa force, c'est d'être lisible : l'adversaire comprend vite qu'une trahison sera punie et qu'une coopération sera rendue. Son point faible, c'est qu'elle ne sait pas sortir d'une série de représailles : une seule trahison peut la faire alterner D/C pendant longtemps. Dans une petite population comme la nôtre, avec peu de stratégies gentilles, je ne suis pas sûr qu'elle gagne.

### 3.4. TESTER, celle qui m'a obligé à trancher

Le cours la décrit en une phrase : « D au premier tour. Si l'adversaire riposte, joue TIT-FOR-TAT ; sinon répète C, C, D. » Au moment de la coder, cette phrase ne suffisait plus. Deux questions se posaient.

**Qu'est-ce qu'une riposte ?** J'ai choisi : l'adversaire joue D au tour juste après un D de TESTER, que ce soit le D d'ouverture ou un D du cycle.

**Une fois en TIT-FOR-TAT, est-ce que TESTER peut redevenir « testeur » ?** J'ai choisi que non : le passage est définitif. La stratégie retient qu'il y a eu riposte jusqu'à la fin de la partie. Il faut donc qu'elle reparte de zéro à chaque nouvelle partie, ce que fait le moteur de Skander.

Pour être sûr de mon code, j'ai déroulé trois parties à la main :

| Adversaire | TESTER joue | Ce qui se passe |
|---|---|---|
| toujours C | D C C D C C D C C | aucune riposte → cycle C, C, D |
| TIT-FOR-TAT | D C D C D C D C | TFT riposte au tour 2 → TESTER copie TFT |
| ALL-D | D C D D D | riposte, puis TFT contre ALL-D |

Le deuxième cas montre un problème. Contre TIT-FOR-TAT, les deux stratégies restent décalées d'un tour et ne reviennent jamais à C/C : elles alternent pendant toute la partie. Le D d'ouverture de TESTER lui coûte donc cher face à une stratégie qui punit. Elle devrait en revanche bien profiter des stratégies qui ne se vengent jamais, en les trahissant un tour sur trois.

**Mon avis :** l'idée de « tester » l'adversaire est maline, mais elle a un coût : avec ma règle, toute stratégie qui punit la fait entrer dans une alternance qui ne s'arrête jamais. Je pense qu'elle sera pénalisée dès que la population contient des stratégies qui se vengent.

### 3.5. JOSS, la trahison sournoise

JOSS se comporte comme TIT-FOR-TAT, mais une fois sur dix, au lieu de coopérer, elle trahit. Dans le code, je calcule d'abord ce que TIT-FOR-TAT jouerait ; si c'est C, je tire au hasard pour savoir si JOSS le remplace par D.

Ces trahisons surprises devraient lui rapporter quelques points contre les stratégies naïves. Mais contre TIT-FOR-TAT, ou contre elle-même, l'enchaînement est prévisible : JOSS trahit, l'adversaire riposte, JOSS recopie la riposte, et les deux alternent D/C, C/D jusqu'à la trahison suivante. C'est le même phénomène que le bruit présenté en cours, sauf qu'ici il est volontaire.

**Mon avis :** JOSS essaie de gagner un peu plus que TIT-FOR-TAT en trichant de temps en temps. Je pense que c'est un mauvais calcul : chaque trahison de 5 points se paie ensuite par plusieurs tours de représailles. Elle illustre bien la règle d'Axelrod « ne pas être trop malin ».

---

## 4. Étape 1 — Le premier tournoi (15/11)

Une fois mes stratégies fusionnées avec le moteur de Skander sur la branche `main`, nous avons pu lancer le vrai tournoi : les cinq stratégies du cours, 5 parties de 200 tours par paire, graine 42.

![Classement de l'étape 1](etape1_classement.png)

### 4.1. TIT-FOR-TAT ne gagne pas

C'est ALL-D qui gagne, et TIT-FOR-TAT ne finit que troisième. Le résultat de 1980 n'est donc pas reproduit. Pour comprendre pourquoi, j'ai regardé le score de TIT-FOR-TAT contre chaque adversaire (total sur les 5 parties, obtenu avec la fonction `run_duels`, voir partie 7) :

| TIT-FOR-TAT contre | Score de TFT | Ce qui se passe |
|---|---|---|
| ALL-D | 1990 | elle perd le premier tour, puis D/D jusqu'à la fin |
| RANDOM | 2498 | ni exploitée, ni récompensée |
| TESTER | 2500 | l'alternance D/C prévue en 3.4 |
| JOSS | 2021 | les représailles en écho prévues en 3.5 |

TIT-FOR-TAT n'atteint jamais 3000 points, c'est-à-dire 3 points par tour : dans cette population, **aucun adversaire ne coopère vraiment avec elle**. TESTER la teste, JOSS triche, RANDOM joue au hasard. Or sa force vient justement de la coopération avec les autres stratégies gentilles.

ALL-D, de son côté, a une proie : contre RANDOM, elle marque 3494 points, son meilleur score. C'est ce qui la fait passer devant tout le monde.

### 4.2. Pourquoi notre résultat diffère de celui de 1980

Je vois deux différences avec le tournoi d'Axelrod :

1. **La taille et la nature de la population.** En 1980, il y avait 14 programmes, et la plupart commençaient par coopérer. TIT-FOR-TAT trouvait donc beaucoup de partenaires avec qui gagner 3 points par tour. Ici, avec cinq stratégies dont aucune n'est vraiment gentille à part elle, elle n'en a aucun.
2. **Les matchs contre soi-même.** Axelrod faisait jouer chaque programme contre son jumeau ; notre tournoi de référence ne le fait pas. Pour vérifier si cela suffisait à expliquer l'écart, Skander a ajouté au moteur une option `self_play`, et j'ai relancé le même tournoi avec ces matchs :

![Classement avec auto-rencontres](etape1_auto_rencontres.png)

TIT-FOR-TAT repasse en tête avec 12 009 points, devant TESTER (11 687) et ALL-D (11 536). L'explication tient en deux chiffres : contre elle-même, TIT-FOR-TAT coopère pendant toute la partie et marque 3000 points sur les 5 parties ; ALL-D contre elle-même ne marque que 2000 points. Ces 1000 points d'écart suffisent à inverser le classement.

Ce résultat rejoint ce que dit le cours : TIT-FOR-TAT n'est pas « la » stratégie optimale, elle prospère seulement s'il y a assez de stratégies qui pensent comme elle.

### 4.3. Ce que je retiens par rapport à mes avis

- ALL-D gagne, mais uniquement grâce à une proie facile (RANDOM) : c'est ce que j'avais envisagé en 3.1.
- RANDOM finit dernière, comme prévu en 3.2.
- Les deux comportements que j'avais repérés en déroulant les parties à la main se retrouvent dans les scores : l'alternance TESTER/TIT-FOR-TAT (2500 de chaque côté) et l'écho JOSS/TIT-FOR-TAT.
- Une surprise : TESTER finit deuxième, devant TIT-FOR-TAT. Son D d'ouverture lui coûte contre TIT-FOR-TAT, mais elle exploite RANDOM et JOSS un peu mieux que TIT-FOR-TAT.

---

## 5. Étape 2 — De nouvelles stratégies

### 5.1. Ma stratégie : GRUDGER

Pour l'étape 2, il fallait une stratégie absente du cours. Je l'ai écrite le 13/11, juste après les cinq stratégies du cours. J'ai hésité entre PAVLOV, TIT-FOR-TWO-TATS, TIT-FOR-TAT généreux et GRUDGER. J'ai choisi **GRUDGER**, « le rancunier ».

Sa règle : je coopère tant que tu n'as jamais trahi ; à ta première trahison, je joue D jusqu'à la fin. Elle vient de James Friedman, qui l'avait soumise au tournoi d'Axelrod ; on la connaît aussi sous le nom de *Grim Trigger*.

Ce qui m'a décidé, c'est qu'elle est l'exact opposé d'une des règles qu'Axelrod tire de son tournoi : « pardonner ». GRUDGER ne pardonne jamais. Elle permet donc de poser une vraie question : si elle finit bien classée, le pardon compte peu dans notre population ; si elle s'effondre, cela confirme Axelrod.

Je m'attends à ce qu'elle joue très bien contre les stratégies gentilles, avec qui elle coopère jusqu'au bout, et correctement contre ALL-D, où elle ne perd que le premier tour, comme TIT-FOR-TAT. En revanche, contre TESTER et JOSS, une seule trahison suffit à la faire basculer en D pour toujours, là où TIT-FOR-TAT aurait pardonné.

### 5.2. La stratégie de Skander : TIT-FOR-TWO-TATS

De son côté, Skander a choisi **TIT-FOR-TWO-TATS**, « donnant-donnant à deux coups ».

Sa règle : je coopère, et je ne trahis que si l'adversaire a joué D **deux fois de suite**. Une trahison isolée est donc laissée passer. C'est une version plus patiente de TIT-FOR-TAT. Elle vient elle aussi des tournois d'Axelrod : après le premier tournoi, Axelrod avait remarqué qu'elle aurait pu le gagner si quelqu'un l'avait proposée, et John Maynard Smith l'a soumise au second tournoi.

En mettant nos deux stratégies côte à côte, je me suis rendu compte qu'elles étaient presque opposées : la mienne ne pardonne jamais, la sienne pardonne facilement. Ça tombait bien pour voir lequel des deux comportements s'en sort le mieux.

Sur le papier, je m'attends à ce qu'elle joue bien contre les stratégies gentilles, comme TIT-FOR-TAT, et surtout mieux que TIT-FOR-TAT contre JOSS : quand JOSS trahit par surprise, TIT-FOR-TWO-TATS ne riposte pas, donc il n'y a pas d'écho de représailles et la coopération reprend tout de suite. Par contre, contre ALL-D, elle perd les deux premiers tours au lieu d'un seul, et une stratégie qui trahit souvent mais jamais deux fois de suite pourrait l'exploiter sans jamais être punie.

**Mon avis :** sa patience est un avantage quand les trahisons sont rares et accidentelles, mais c'est aussi une porte ouverte pour les stratégies qui calculent leurs trahisons.

### 5.3. Le tournoi à sept stratégies (15/11)

On a relancé le tournoi avec les sept stratégies, en gardant exactement le même protocole qu'à l'étape 1.

![Classement de l'étape 2](etape2_classement.png)

Je ne m'attendais pas à ça : **GRUDGER finit première**. TIT-FOR-TAT remonte à la deuxième place, et ALL-D, qui avait gagné l'étape 1, tombe à la sixième.

Pour comprendre pourquoi ma stratégie gagne, j'ai affiché le score de chaque duel avec la fonction `run_duels` :

![Scores des duels de l'étape 2](etape2_duels.png)

Voici ce que ça donne pour GRUDGER (ligne GRUDGER de la capture) :

| GRUDGER contre | Score de GRUDGER | Ce qui se passe |
|---|---|---|
| TIT-FOR-TAT, TIT-FOR-TWO-TATS | 3000 | elles coopèrent du début à la fin |
| RANDOM | 3480 | RANDOM trahit vite, GRUDGER passe en D pour toujours et en profite |
| ALL-D | 1990 | elle perd seulement le premier tour |
| TESTER | 2005 | le D du premier tour de TESTER la fait basculer |
| JOSS | 2018 | la première trahison de JOSS suffit |

En fait, GRUDGER fait un peu les deux à la fois : avec les stratégies gentilles, elle coopère comme TIT-FOR-TAT, et contre RANDOM, elle trahit tout le temps comme ALL-D (3480 points, alors que TIT-FOR-TAT n'en fait que 2498). Ses deux points faibles, TESTER et JOSS, sont bien ceux que j'avais prévus en 5.1, mais ils ne lui font pas perdre assez de points pour la faire descendre.

### 5.4. Ce qui a changé par rapport à l'étape 1

**Les nouvelles stratégies ne donnent rien à ALL-D.** ALL-D exploite toujours RANDOM (3494 points), mais les deux nouvelles stratégies commencent par coopérer et se défendent : ALL-D ne fait qu'environ 2000 points contre chacune. Par contre, entre elles, les stratégies gentilles se font 3000 points. C'est justement ce qui manquait à TIT-FOR-TAT à l'étape 1 : maintenant elle a des partenaires, et elle repasse devant ALL-D. Ça rejoint ce que je pensais en partie 4 : TIT-FOR-TAT a besoin d'autres stratégies qui coopèrent pour bien marcher.

**TESTER profite de TIT-FOR-TWO-TATS.** En regardant les duels, j'ai vu que TESTER fait 3670 points contre elle, son meilleur score. En déroulant la partie, j'ai compris pourquoi : le cycle de TESTER, C, C, D, ne contient jamais deux D de suite. Du coup, TIT-FOR-TWO-TATS ne riposte jamais et se fait avoir pendant toute la partie. Être patient, ça coûte cher contre quelqu'un qui trahit souvent mais jamais deux fois d'affilée.

**Mais la patience paie contre JOSS.** Comme je l'attendais en 5.2, TIT-FOR-TWO-TATS fait 2629 points contre JOSS, alors que TIT-FOR-TAT n'en fait que 2046 : quand JOSS trahit par surprise, elle ne riposte pas, et la coopération reprend sans écho de représailles. Sa patience l'aide contre les trahisons rares, et la dessert contre les trahisons régulières.

**Le pardon ne gagne pas ici.** J'avais choisi GRUDGER pour tester la règle « pardonner » d'Axelrod, et dans notre tournoi, c'est la stratégie rancunière qui gagne, alors que la plus patiente finit quatrième. Mon explication : comme il n'y a aucune erreur, les stratégies gentilles ne trahissent jamais, donc GRUDGER n'a jamais besoin de pardonner. Je pense que ça changera si un coup peut être inversé par erreur : une seule erreur et GRUDGER trahit jusqu'à la fin.

Avec les auto-rencontres, le haut du classement ne change pas : GRUDGER (18 493) reste devant TIT-FOR-TAT (18 009).

---

## 6. Étape 3 — Modifier le tournoi

Pour l'étape 3, il fallait appliquer au moins deux modifications au tournoi. Avec Skander, on a choisi le **bruit** et l'**horizon inconnu**. Pour le code, on s'est réparti le travail : Skander programme le bruit, moi l'horizon inconnu. Mais chacun fait ses propres prédictions et sa propre analyse pour les deux.

Pour chaque modification, j'ai écrit ma prédiction ici avant de lancer quoi que ce soit.

### 6.1. Le bruit

Avec le bruit, chaque coup peut être inversé par erreur avec une petite probabilité (5 %, l'exemple de l'énoncé) : une stratégie veut jouer C, mais c'est D qui part, ou l'inverse.

On l'a choisi parce que le cours en parle (deux TIT-FOR-TAT qui se punissent en écho après une seule erreur), et surtout parce que c'est le vrai test pour ma stratégie : à l'étape 2, GRUDGER a gagné parce que personne ne trahissait par erreur.

**Ma prédiction (écrite avant de lancer le tournoi) :**

Avec des erreurs, GRUDGER perdra sa première place : une seule erreur suffit à la rendre rancunière pour toute la partie, même contre les stratégies gentilles. C'est TIT-FOR-TWO-TATS qui gagnera, car elle laisse passer une trahison isolée.

### 6.2. L'horizon inconnu

Au lieu de jouer exactement 200 tours, après chaque tour la partie continue avec une probabilité w. Personne ne sait donc quand elle va s'arrêter.

J'ai choisi cette modification parce qu'elle touche directement l'argument du cours en faveur d'ALL-D : la récurrence à rebours ne marche que si on connaît le dernier tour. Le cours dit aussi que l'infini n'est pas nécessaire pour coopérer, il suffit que les joueurs sachent qu'ils ont de bonnes chances de se revoir. Je voulais voir ce que ça change concrètement dans notre tournoi.

Pour pouvoir comparer avec l'étape 2, j'ai choisi **w = 0,995** : une partie dure alors 200 tours en moyenne (1 / (1 − w) = 200), comme avant. La seule différence, c'est que certaines parties seront plus courtes et d'autres plus longues.

**Ma prédiction (écrite avant de lancer le tournoi) :**

Je pense que l'horizon inconnu va aider ALL-D. Les stratégies jouent pareil qu'avant, mais avec w, certaines parties vont être très courtes. Et dans une partie courte, le premier tour compte beaucoup : ALL-D le gagne contre les gentilles (5 points pour elle, 0 pour l'autre), et après il n'y a pas assez de tours pour que TIT-FOR-TAT ou GRUDGER rattrapent en coopérant. Sur 200 tours, perdre le premier tour ce n'est presque rien, mais sur 10 tours ça fait une vraie différence.

Du coup, je m'attends à ce qu'ALL-D remonte beaucoup par rapport à l'étape 2 (elle était sixième) et qu'elle passe devant les stratégies gentilles.

**Implémentation et test**

J'ai ajouté au moteur un paramètre `continuation` (c'est w). Après chaque tour, on tire un nombre au hasard : s'il dépasse w, la partie s'arrête. Sans ce paramètre, le moteur joue toujours exactement 200 tours, donc les étapes 1 et 2 ne changent pas.

J'ai fait un choix : ce tirage utilise son propre générateur, qui dépend seulement de la graine de la partie. Du coup, la partie n°1 a la même longueur pour toutes les paires, la partie n°2 aussi, etc. Je l'ai fait exprès : sinon, une stratégie pourrait gagner juste parce qu'elle est tombée sur des parties plus longues, et la comparaison ne serait plus juste.

Pour vérifier, j'ai écrit un test : avec w = 0, une partie dure bien un seul tour ; la longueur est la même quelles que soient les stratégies ; et sur 2000 parties avec w = 0,995, la moyenne est de 204 tours, avec des parties d'un seul tour et d'autres de plus de 1500 tours.

**Résultats**

![Classement avec l'horizon inconnu](etape3_horizon.png)

Le classement est **exactement le même qu'à l'étape 2** : GRUDGER reste première et ALL-D reste sixième. Les scores sont plus élevés, mais c'est seulement parce que les parties ont été plus longues : 1764 tours au total sur les 5 parties, au lieu de 1000.

**Comparaison avec ma prédiction**

Ma prédiction était fausse : ALL-D n'a pas remonté du tout. En cherchant pourquoi, j'ai regardé la longueur des 5 parties : 618, 137, 291, 401 et 317 tours. Il n'y a eu **aucune partie courte**. Or mon raisonnement reposait justement sur les parties courtes. Sur 137 tours ou plus, le premier tour gagné par ALL-D (5 points contre 0) ne pèse presque rien face aux 3 points par tour que les stratégies gentilles se donnent entre elles.

J'ai relancé avec d'autres graines (0, 100, 1000) : le classement ne bouge pas. Ce n'est donc pas un hasard de la graine 42. Avec w = 0,995, les parties très courtes sont rares, et nos stratégies jouent exactement pareil quelle que soit la longueur, puisqu'aucune ne regarde le numéro du tour.

**Expérience complémentaire : à partir de quand ALL-D gagne-t-elle ?**

Je voulais savoir si mon idée était fausse, ou si les parties n'étaient juste pas assez courtes. J'ai donc relancé le tournoi avec des w plus petits. Comme les longueurs varient beaucoup d'une partie à l'autre, j'ai pris **200 parties par paire** au lieu de 5 pour que le hasard des longueurs s'équilibre. Cette expérience sort donc du protocole de référence, elle sert seulement à tester mon raisonnement.

![Classement selon w](etape3_horizon_w.png)

| w | Longueur moyenne | Rang d'ALL-D |
|---|---|---|
| 0,995 | environ 200 tours | 6e |
| 0,9 | environ 10 tours | 3e |
| 0,8 | environ 5 tours | 1re |
| 0,5 | environ 2 tours | 1re |

Mon idée n'était donc pas complètement fausse : quand les parties sont vraiment courtes, le premier tour pèse beaucoup et ALL-D finit par gagner. Mais il faut des parties d'environ 5 tours en moyenne, très loin des 200 tours de notre protocole.

**Ce que j'en retiens**

Je me suis trompé sur l'ordre de grandeur, pas sur le mécanisme. Ça rejoint le cours : pour que la coopération l'emporte, il n'est pas nécessaire que le jeu soit infini, il suffit que « le futur pèse assez lourd », c'est-à-dire que les joueurs aient de bonnes chances de se revoir. Avec w = 0,995, c'est largement le cas ; avec w = 0,8, ce n'est plus le cas, et trahir tout de suite devient la meilleure option.

---

## 7. Impasses

- **La règle de TESTER ne suffisait pas.** Au départ, je pensais coder TESTER directement à partir de la phrase du cours. En réalité, elle ne dit pas ce qu'est une riposte ni si le passage en TIT-FOR-TAT est définitif. J'ai dû faire deux choix, expliqués en 3.4. En déroulant les parties à la main, j'ai vu qu'avec ces choix, TESTER contre TIT-FOR-TAT ne revient jamais à la coopération. Une autre interprétation aurait pu donner un comportement très différent.
- **Des scores de duels faux de quelques points.** Dans une première version de ce journal, le score de TIT-FOR-TAT contre RANDOM était 2494, et la somme de ses duels ne donnait pas son total du classement (4 points d'écart). Skander l'a remarqué en relisant. En cherchant, j'ai compris que j'avais recalculé les duels en mettant TIT-FOR-TAT en premier joueur, alors que dans le tournoi c'est RANDOM qui joue en premier. Or le moteur donne une graine différente à chaque joueur : en inversant l'ordre, RANDOM ne tire plus les mêmes coups. Pour que les chiffres sortent du code du dépôt et plus d'un calcul à côté, j'ai ajouté au moteur une fonction `run_duels`. Elle fait jouer les stratégies exactement comme le tournoi (même ordre, mêmes graines, même option `self_play`), mais elle renvoie le score de chaque duel au lieu du total. J'ai aussi ajouté un test qui vérifie que, pour chaque stratégie, la somme de ses duels est égale à son score dans le classement, avec et sans auto-rencontres. Tous les scores de duels de ce journal viennent maintenant de cette fonction.
