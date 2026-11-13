#Le fichier de gestion du jeu de moteur

def get_payoffs(action1, action2):
    if action1 == "C" and action2 == "C":
        return (3,3)
    elif action1 == "C" and action2 == "D":
        return (0,5)
    elif action1 == "D" and action2 == "C":
        return (5,0)
    elif action1 == "D" and action2 == "D":
        return (2,2)
    else:
        raise ValueError("L'une des actions est incorrecte !")



assert get_payoffs("C", "C") == (3, 3)
assert get_payoffs("C", "D") == (0, 5)
assert get_payoffs("D", "C") == (5, 0)
assert get_payoffs("D", "D") == (2, 2)
try:
    get_payoffs("X", "C")
    assert False, "Une exception était attendue"
except ValueError:
    print("Test des actions invalides réussi !")

print("Tous les tests sont réussis !")
