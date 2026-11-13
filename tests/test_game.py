from engine.game import get_payoffs, play_game
from engine.tournament import run_tournament

class AlwaysCooperate:
    nom = "ALL-C"
    def jouer(self, mes_coups, ses_coups, rng):
        return "C"

class AlwaysDefect:
    nom = "ALL-D"
    def jouer(self, mes_coups, ses_coups, rng):
        return "D"

class TitForTat:
    nom = "TIT FOR TAT"
    def jouer(self, mes_coups, ses_coups, rng):
        return "C" if not ses_coups else ses_coups[-1]


def test_payoffs():
    assert get_payoffs("C", "C") == (3, 3)
    assert get_payoffs("C", "D") == (0, 5)
    assert get_payoffs("D", "C") == (5, 0)
    assert get_payoffs("D", "D") == (2, 2)


def test_games():
    assert play_game(AlwaysCooperate(), AlwaysCooperate()) == (600, 600)
    assert play_game(AlwaysDefect(), AlwaysDefect()) == (400, 400)
    assert play_game(AlwaysDefect(), AlwaysCooperate()) == (1000, 0)
    assert play_game(AlwaysDefect(), TitForTat()) == (403, 398)
    assert play_game(TitForTat(), TitForTat()) == (600, 600)


if __name__ == "__main__":
    test_payoffs()
    test_games()
    print("Tous les tests sont réussis !")

    ranking = run_tournament([AlwaysCooperate, AlwaysDefect, TitForTat])
    for name, score in ranking:
        print(f"{name}: {score} points")