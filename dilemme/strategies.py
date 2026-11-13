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
