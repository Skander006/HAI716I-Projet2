from strategies_base.strategies import TitForTwoTats

def test_tit_for_two_tats():
    strategie = TitForTwoTats()

    assert strategie.jouer([], [], None) == "C"
    assert strategie.jouer([], ["D"], None) == "C"
    assert strategie.jouer([], ["C", "D"], None) == "C"
    assert strategie.jouer([], ["D", "D"], None) == "D"
    assert strategie.jouer([], ["D", "C"], None) == "C"
    assert strategie.jouer([], ["D", "D", "D"], None) == "D"

    print("Test TIT-FOR-TWO-TATS réussi !")

if __name__ == "__main__":
    test_tit_for_two_tats()