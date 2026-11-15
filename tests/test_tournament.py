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

def test_self_play():
    sans = dict(run_tournament([TitForTat, AlwaysDefect],games_per_pair=1,rounds=10))
    avec = dict(run_tournament([TitForTat, AlwaysDefect],games_per_pair=1,rounds=10,self_play=True))

    assert sans == {"TIT-FOR-TAT": 18, "ALL-D": 23}
    assert avec == {"TIT-FOR-TAT": 48, "ALL-D": 43}

    print("\n========== TEST DES AUTO-RENCONTRES ==========")
    print("\nSANS AUTO-RENCONTRES :")
    for rang, (nom, score) in enumerate(sorted(sans.items(), key=lambda x: x[1], reverse=True), 1):
        print(f"{rang}. {nom} : {score} points")
    print("\nAVEC AUTO-RENCONTRES :")
    for rang, (nom, score) in enumerate(sorted(avec.items(), key=lambda x: x[1], reverse=True), 1):
        print(f"{rang}. {nom} : {score} points")
    print("\nTest des auto-rencontres réussi !")

if __name__ == "__main__":
    test_tournament_scores()
    test_tournament_ranking()
    test_reproducibility()
    test_games_per_pair()
    test_self_play()
    print("\nTous les tests du tournoi sont réussis !")
