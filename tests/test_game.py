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


def longueur(seed, continuation):
    return play_game(AlwaysCooperate(), AlwaysCooperate(), seed=seed, continuation=continuation)[0] // 3

class AlwaysCooperate:
    nom = "ALL-C"

    def jouer(self, mes_coups, ses_coups, rng):
        return "C"

def test_noise_zero():
    s1, s2 = play_game(AlwaysCooperate(),AlwaysCooperate(),rounds=200,noise=0.0)
    assert (s1, s2) == (600, 600)
def test_noise_one():
    s1, s2 = play_game(AlwaysCooperate(),AlwaysCooperate(),rounds=200,noise=1.0)
    assert (s1, s2) == (400, 400)

def test_noise_reproducibility():
    result1 = play_game(AlwaysCooperate(),AlwaysCooperate(),rounds=200,seed=42,noise=0.05)
    result2 = play_game(AlwaysCooperate(),AlwaysCooperate(),rounds=200,seed=42,noise=0.05)
    assert result1 == result2

def test_horizon_inconnu():
    assert play_game(AlwaysCooperate(), AlwaysCooperate(), continuation=0) == (3, 3)
    assert play_game(AlwaysDefect(), TitForTat(), continuation=0) == (5, 0)

    for seed in range(20):
        assert play_game(AlwaysDefect(), AlwaysDefect(), seed=seed, continuation=0.995)[0] // 2 == longueur(seed, 0.995)
        assert longueur(seed, 0.995) == longueur(seed, 0.995)

    longueurs = [longueur(seed, 0.995) for seed in range(2000)]
    moyenne = sum(longueurs) / len(longueurs)
    assert 190 < moyenne < 220
    assert min(longueurs) < 20 and max(longueurs) > 600

    print("\n========== TEST DE L'HORIZON INCONNU ==========")
    print("w = 0 : une seule partie d'un tour ->", play_game(AlwaysDefect(), TitForTat(), continuation=0))
    print("Longueurs des 5 parties du tournoi (graines 42 a 46, w = 0.995) :", [longueur(42 + g, 0.995) for g in range(5)])
    print(f"Longueur moyenne sur 2000 parties : {moyenne:.1f} tours (min {min(longueurs)}, max {max(longueurs)})")
    print("Test de l'horizon inconnu reussi !")


if __name__ == "__main__":
    test_payoffs()
    test_games()
    test_horizon_inconnu()
    test_noise_one()
    test_noise_zero()
    test_noise_reproducibility()
    print("Tous les tests sont réussis !")

    ranking = run_tournament([AlwaysCooperate, AlwaysDefect, TitForTat])
    for name, score in ranking:
        print(f"{name}: {score} points")