import random
from strategies_base.strategies import (AllD,Random, TitForTat,Tester,Joss,Grudger,TitForTwoTats)


class FakeRNG:
    def __init__(self, valeur):
        self.valeur = valeur

    def random(self):
        return self.valeur


def test_tit_for_two_tats():
    strategie = TitForTwoTats()

    assert strategie.jouer([], [], None) == "C"
    assert strategie.jouer([], ["D"], None) == "C"
    assert strategie.jouer([], ["C", "D"], None) == "C"
    assert strategie.jouer([], ["D", "D"], None) == "D"
    assert strategie.jouer([], ["D", "C"], None) == "C"
    assert strategie.jouer([], ["D", "D", "D"], None) == "D"

    print("Test TIT-FOR-TWO-TATS réussi !")

def test_All_D():
    strategie = AllD()

    assert strategie.jouer([], [], None) == "D"
    assert strategie.jouer([], ["C"], None) == "D"
    assert strategie.jouer([], ["D"], None) == "D"
    assert strategie.jouer([], ["C", "C"], None) == "D"
    assert strategie.jouer([], ["C", "C", "C"], None) == "D"
    assert strategie.jouer([], ["D", "D"], None) == "D"
    assert strategie.jouer([], ["D", "D", "D"], None) == "D"
    assert strategie.jouer(["C"], ["C"], None) == "D"

    print("Test ALL-D réussi !")

def test_random():
    strategie = Random()

    assert strategie.jouer([], [], FakeRNG(0.0)) == "C"
    assert strategie.jouer([], [], FakeRNG(0.49)) == "C"
    assert strategie.jouer([], [], FakeRNG(0.5)) == "D"
    assert strategie.jouer([], [], FakeRNG(0.99)) == "D"

    rng1 = random.Random(42)
    rng2 = random.Random(42)
    coups1 = [strategie.jouer([], [], rng1) for _ in range(100)]
    coups2 = [strategie.jouer([], [], rng2) for _ in range(100)]

    assert coups1 == coups2
    assert "C" in coups1
    assert "D" in coups1

    print("Test RANDOM réussi !")

def test_tit_for_tat():
    strategie = TitForTat()

    assert strategie.jouer([], [], None) == "C"
    assert strategie.jouer(["C"], ["C"], None) == "C"
    assert strategie.jouer(["C"], ["D"], None) == "D"
    assert strategie.jouer(["C", "D"], ["D", "C"], None) == "C"
    assert strategie.jouer(["C", "C"], ["C", "D"], None) == "D"
    assert strategie.jouer(["D", "D"], ["D", "D"], None) == "D"

    print("Test TIT-FOR-TAT réussi !")

def test_tester():
    strategie = Tester()
    assert strategie.jouer([], [], None) == "D"
    strategie = Tester()
    mes_coups = []
    ses_coups = []
    for coup_attendu in ["D", "C", "C", "D", "C", "C"]:
        coup = strategie.jouer(mes_coups, ses_coups, None)
        assert coup == coup_attendu
        mes_coups.append(coup)
        ses_coups.append("C")

    strategie = Tester()
    assert strategie.jouer([], [], None) == "D"
    assert strategie.jouer(["D", "C"], ["C", "D"], None) == "D"
    assert strategie.riposte is True
    assert strategie.jouer(["D", "C", "D"], ["C", "D", "C"], None) == "C"

    print("Test TESTER réussi !")

def test_joss():
    strategie = Joss()

    # Premier tour : coopération normalement prévue
    assert strategie.jouer([], [], FakeRNG(0.5)) == "C"

    # Défection aléatoire avec probabilité de 10 %
    assert strategie.jouer([], [], FakeRNG(0.05)) == "D"
    assert strategie.jouer([], [], FakeRNG(0.1)) == "C"

    # Si l'adversaire a joué D, JOSS riposte
    assert strategie.jouer(["C"], ["D"], FakeRNG(0.05)) == "D"
    assert strategie.jouer(["C"], ["D"], FakeRNG(0.9)) == "D"

    # Si l'adversaire a joué C, la décision
    # dépend du générateur aléatoire.
    assert strategie.jouer(["C"], ["C"], FakeRNG(0.05)) == "D"
    assert strategie.jouer(["C"], ["C"], FakeRNG(0.5)) == "C"

    print("Test JOSS réussi !")


def test_grudger():
    strategie = Grudger()
    assert strategie.jouer([], [], None) == "C"
    assert strategie.jouer(["C"], ["C"], None) == "C"
    assert strategie.jouer(["C", "C"], ["C", "C"], None) == "C"
    assert strategie.jouer(["C"], ["D"], None) == "D"
    assert strategie.jouer(["C", "D", "D"], ["D", "C", "C"], None) == "D"
    assert strategie.jouer(["C"] * 5, ["C", "C", "D", "C", "C"], None) == "D"
    print("Test GRUDGER réussi !")



if __name__ == "__main__":
    test_tit_for_two_tats()
    test_All_D()
    test_random()
    test_tit_for_tat()
    test_tester()
    test_joss()
    test_grudger()