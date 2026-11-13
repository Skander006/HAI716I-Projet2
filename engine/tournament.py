
from engine.game import play_game


def run_tournament(strategies, games_per_pair=5, rounds=200, seed=42):
    # Initialiser les scores
    scores = {strategy.nom: 0 for strategy in strategies}
    # Parcourir toutes les paires de stratégies
    for i in range(len(strategies)):
        for j in range(i + 1, len(strategies)):
            strategy1 = strategies[i]
            strategy2 = strategies[j]
            # Faire jouer chaque paire 5 fois
            for game in range(games_per_pair):
                score1, score2 = play_game(strategy1(),strategy2(),rounds=rounds,seed=seed + game)
                # Cumuler les points
                scores[strategy1.nom] += score1
                scores[strategy2.nom] += score2
    # Classer les stratégies par score décroissant
    ranking = sorted(scores.items(),key=lambda item: item[1],reverse=True)
    return ranking
