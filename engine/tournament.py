
from engine.game import play_game

def run_tournament(strategies, games_per_pair=5, rounds=200, seed=42, self_play = False):
    # Initialiser les scores
    scores = {strategy.nom: 0 for strategy in strategies}
    for i in range(len(strategies)):
        start = i if self_play else i + 1
        for j in range(start, len(strategies)):
            strategy1 = strategies[i]
            strategy2 = strategies[j]
            # Faire jouer chaque paire 5 fois
            for game in range(games_per_pair):
                score1, score2 = play_game(strategy1(),strategy2(),rounds=rounds,seed=seed + game)
                scores[strategy1.nom] += score1
                if i!=j :
                    scores[strategy2.nom] += score2
    # Classer les stratégies par score décroissant
    ranking = sorted(scores.items(),key=lambda item: item[1],reverse=True)
    return ranking


def run_duels(strategies, games_per_pair=5, rounds=200, seed=42, self_play=False):
    duels = {}
    for i in range(len(strategies)):
        start = i if self_play else i + 1
        for j in range(start, len(strategies)):
            strategy1 = strategies[i]
            strategy2 = strategies[j]
            total1, total2 = 0, 0
            for game in range(games_per_pair):
                score1, score2 = play_game(strategy1(), strategy2(), rounds=rounds, seed=seed + game)
                total1 += score1
                total2 += score2
            duels[(strategy1.nom, strategy2.nom)] = total1
            if i != j:
                duels[(strategy2.nom, strategy1.nom)] = total2
    return duels
