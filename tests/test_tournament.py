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
    nom = "TIT-FOR-TAT"
    def jouer(self, mes_coups, ses_coups, rng):
        return "C" if not ses_coups else ses_coups[-1]

def test_tournament_scores():
    ranking = run_tournament([AlwaysCooperate, AlwaysDefect, TitForTat])
    scores = dict(ranking)
    assert scores["ALL-C"] == 3000
    assert scores["ALL-D"] == 7015
    assert scores["TIT-FOR-TAT"] == 4990
    print("Test des scores du tournoi réussi !")

def test_tournament_ranking():
    ranking = run_tournament([AlwaysCooperate, AlwaysDefect, TitForTat])
    names = [name for name, score in ranking]
    assert names == ["ALL-D", "TIT-FOR-TAT", "ALL-C"]
    print("Test du classement réussi !")

def test_reproducibility():
    strategies = [AlwaysCooperate, AlwaysDefect, TitForTat]
    ranking1 = run_tournament(strategies, seed=42)
    ranking2 = run_tournament(strategies, seed=42)
    assert ranking1 == ranking2
    print("Test de reproductibilité réussi !")

def test_games_per_pair():
    ranking = run_tournament([AlwaysCooperate, AlwaysDefect],games_per_pair=1,rounds=10)
    scores = dict(ranking)
    assert scores["ALL-C"] == 0
    assert scores["ALL-D"] == 50
    print("Test du nombre de parties réussi !")

if __name__ == "__main__":
    test_tournament_scores()
    test_tournament_ranking()
    test_reproducibility()
    test_games_per_pair()
    print("\nTous les tests du tournoi sont réussis !")
