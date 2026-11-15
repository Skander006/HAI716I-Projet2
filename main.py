from engine.tournament import run_tournament
from strategies_base.strategies import (AllD, Random, TitForTat, Tester,Joss, Grudger, TitForTwoTats)
from engine.tournament import run_duels

strategies = [AllD, Random, TitForTat, Tester,Joss, Grudger, TitForTwoTats]
resultats = run_tournament(strategies)

print("\n=== CLASSEMENT ÉTAPE 2 ===")

for rang, (nom, score) in enumerate(sorted(resultats, key=lambda x: x[1], reverse=True),start=1):
    print(f"{rang}. {nom:<20} : {score} points")

duels = run_duels(strategies)

print("\n" + "=" * 115)
print("TABLEAU DES DUELS — ÉTAPE 2")
print("=" * 115)

largeur = 19

print(f"{'Stratégie':<{largeur}}", end="")
for adversaire in strategies:
    print(f"{adversaire.nom:>{largeur}}", end="")
print(f"{'TOTAL':>10}")

print("-" * (largeur * (len(strategies) + 1) + 10))

for strategie in strategies:
    print(f"{strategie.nom:<{largeur}}", end="")

    total = 0

    for adversaire in strategies:
        if strategie.nom == adversaire.nom:
            print(f"{'—':>{largeur}}", end="")
        else:
            score = duels[(strategie.nom, adversaire.nom)]
            total += score
            print(f"{score:>{largeur}}", end="")

    print(f"{total:>10}")

print("\n=== TOURNOI SANS BRUIT (0 %) ===")
resultats_sans_bruit = run_tournament(strategies,games_per_pair=5,rounds=200,seed=42,self_play=False,noise=0.0)
for rang, (nom, score) in enumerate(resultats_sans_bruit, 1):
    print(f"{rang}. {nom:<20} : {score} points")

print("\n=== TOURNOI AVEC BRUIT (5 %) ===")
resultats_avec_bruit = run_tournament(strategies,games_per_pair=5,rounds=200,seed=42,self_play=False,noise=0.05)
for rang, (nom, score) in enumerate(resultats_avec_bruit, 1):
    print(f"{rang}. {nom:<20} : {score} points")


duels_bruit = run_duels(strategies,games_per_pair=5,rounds=200,seed=42,self_play=False,noise=0.05)
noms = [strategie.nom for strategie in strategies]
print("\n=== DUELS AVEC BRUIT DE 5 % ===")
print(f"{'Stratégie':<20}", end="")
for nom in noms:
    print(f"{nom[:10]:>12}", end="")
print()
for nom1 in noms:
    print(f"{nom1:<20}", end="")
    for nom2 in noms:
        if nom1 == nom2:
            print(f"{'-':>12}", end="")
        else:
            print(f"{duels_bruit[(nom1, nom2)]:>12}", end="")
    print()