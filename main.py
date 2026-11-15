from engine.tournament import run_tournament
from strategies_base.strategies import (AllD, Random, TitForTat, Tester,Joss, Grudger, TitForTwoTats)
from engine.tournament import run_duels

strategies_cours = [AllD, Random, TitForTat, Tester, Joss]

print("\n=== CLASSEMENT ÉTAPE 1 (5 stratégies du cours, sans auto-rencontres) ===")
resultats_etape1 = run_tournament(strategies_cours,games_per_pair=5,rounds=200,seed=42,self_play=False)
for rang, (nom, score) in enumerate(resultats_etape1, 1):
    print(f"{rang}. {nom:<20} : {score} points")

print("\n=== CLASSEMENT ÉTAPE 1 (5 stratégies du cours, avec auto-rencontres) ===")
resultats_etape1_soi = run_tournament(strategies_cours,games_per_pair=5,rounds=200,seed=42,self_play=True)
for rang, (nom, score) in enumerate(resultats_etape1_soi, 1):
    print(f"{rang}. {nom:<20} : {score} points")

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

print("\n=== CLASSEMENT ÉTAPE 2 (avec auto-rencontres) ===")
resultats_etape2_soi = run_tournament(strategies,games_per_pair=5,rounds=200,seed=42,self_play=True)
for rang, (nom, score) in enumerate(resultats_etape2_soi, 1):
    print(f"{rang}. {nom:<20} : {score} points")

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
print("\n=== TOURNOI AVEC HORIZON INCONNU (w = 0.995) ===")
resultats_horizon = run_tournament(strategies,games_per_pair=5,rounds=200,seed=42,self_play=False,continuation=0.995)
for rang, (nom, score) in enumerate(resultats_horizon, 1):
    print(f"{rang}. {nom:<20} : {score} points")

duels_horizon = run_duels(strategies,games_per_pair=5,rounds=200,seed=42,self_play=False,continuation=0.995)
print("\n=== DUELS AVEC HORIZON INCONNU (w = 0.995) ===")
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
            print(f"{duels_horizon[(nom1, nom2)]:>12}", end="")
    print()

print("\n=== HORIZON INCONNU : EXPERIENCE COMPLEMENTAIRE (200 parties par paire) ===")
for w in (0.995, 0.9, 0.8, 0.5):
    resultats_w = run_tournament(strategies,games_per_pair=200,seed=42,self_play=False,continuation=w)
    classement = [nom for nom, score in resultats_w]
    print(f"\nw = {w} (environ {round(1 / (1 - w))} tours par partie) : ALL-D est {classement.index('ALL-D') + 1}e")
    print("   " + " > ".join(classement))

print("\n=== BRUIT 5 % : CLASSEMENT AVEC D'AUTRES GRAINES ===")
for graine in range(10):
    classement = [nom for nom, score in run_tournament(strategies,games_per_pair=5,rounds=200,seed=graine,self_play=False,noise=0.05)]
    print(f"graine {graine} : " + " > ".join(classement))

print("\n=== HORIZON INCONNU (w = 0.995) : CLASSEMENT AVEC D'AUTRES GRAINES ===")
for graine in (0, 100, 1000):
    classement = [nom for nom, score in run_tournament(strategies,games_per_pair=5,rounds=200,seed=graine,self_play=False,continuation=0.995)]
    print(f"graine {graine} : " + " > ".join(classement))
