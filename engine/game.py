#Le fichier de gestion du jeu de moteur
import random

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


def play_game(strategy1, strategy2,rounds = 200, seed = 42):
    history1, history2 = [], []
    score1, score2 = 0, 0
    rng1 = random.Random(seed)
    rng2 = random.Random(seed + 1)
    for i in range (rounds):
        action1 = strategy1.jouer(history1, history2, rng1)
        action2 = strategy2.jouer(history2, history1, rng2)
        history1.append(action1)
        history2.append(action2)
        gain1, gain2 = get_payoffs(action1, action2)
        score1 += gain1
        score2 += gain2
    return score1, score2
    
    

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
