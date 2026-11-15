"""Stratégies du dilemme du prisonnier itéré.

Chaque stratégie est une classe avec :
  - nom : le nom affiché dans le classement
  - jouer(mes_coups, ses_coups, rng) -> 'C' ou 'D'
    mes_coups / ses_coups : listes des coups déjà joués (tour 1 en premier)
    rng : générateur aléatoire (random.Random) créé par le moteur avec la graine
"""

C, D = 'C', 'D'


class AllD:
    """Toujours D : la stratégie « rationnelle » de la récurrence à rebours."""
    nom = 'ALL-D'

    def jouer(self, mes_coups, ses_coups, rng):
        return D


class Random:
    nom = 'RANDOM'

    def jouer(self, mes_coups, ses_coups, rng):
        return C if rng.random() < 0.5 else D


class TitForTat:
    nom = 'TIT-FOR-TAT'

    def jouer(self, mes_coups, ses_coups, rng):
        if not ses_coups:
            return C
        return ses_coups[-1]


class Tester:
    nom = 'TESTER'

    def __init__(self):
        self.riposte = False

    def jouer(self, mes_coups, ses_coups, rng):
        tour = len(mes_coups) + 1
        if tour == 1:
            return D
        if mes_coups[-2:-1] == [D] and ses_coups[-1] == D:
            self.riposte = True
        if self.riposte:
            return ses_coups[-1]
        return D if (tour - 1) % 3 == 0 else C


class Joss:
    nom = 'JOSS'

    def jouer(self, mes_coups, ses_coups, rng):
        coup = ses_coups[-1] if ses_coups else C
        if coup == C and rng.random() < 0.1:
            return D
        return coup


class Grudger:
    nom = 'GRUDGER'

    def jouer(self, mes_coups, ses_coups, rng):
        if D in ses_coups:
            return D
        return C

class TitForTwoTats:
    nom = 'TIT-FOR-TWO-TATS'

    def jouer(self, mes_coups, ses_coups, rng):
        if len(ses_coups) < 2:
            return C

        if ses_coups[-1] == D and ses_coups[-2] == D:
            return D
        return C

