import numpy as np
from scipy.stats import ttest_rel


def dcg_at_k(ranking, relevance_scores, k):
    """
    Computes the Discounted Cumulative Gain (DCG) at rank k.
    ranking: A list of ranked teams (team names or IDs).
    relevance_scores: A list of relevance scores corresponding to each team.
    k: The number of top ranks to consider for the DCG.
    """
    dcg = 0
    for i in range(k):
        relevance = relevance_scores[i]  # Get relevance score for this team
        dcg += relevance / np.log2(i + 2)  # +2 for log(i+1) starting from i=0
    return dcg

def ndcg(r_ap, ranking):  # Convert AP rankings to numpy array
    total = 0

    for r in range(len(ranking)):
        # Find the relevance score (higher ranks get higher scores)
        indices = r_ap.index(ranking[r]) if ranking[r] in r_ap else len(r_ap)
        relevance = len(r_ap) - indices

        # Apply logarithmic discounting (except for rank 0)
        if r > 0:
            relevance /= np.log2(r + 1)

        total += relevance

    return total

def compare_rankings(r_ap, rankings):
    ideal = ndcg(r_ap, r_ap)  # Ideal NCTG score (when ranking is perfect)
    print(ideal)
    ndcg_scores = [ndcg(r_ap, r) / ideal for r in rankings]

    return ideal, ndcg_scores

def helper(ranking, records, team_games, long_rankings=None):
    team_names = {records[ranking[j]][0]: j for j in range(len(ranking))}
    if long_rankings is not None:
        full_team_names = {records[long_rankings[j]][0]: j for j in range(len(records))}
        upsets = 0
        total_games = 0
        top_25 = 0
        total_top_25 = 0
        for team in team_names:
            for game in team_games[team]:
                total_top_25 += 1
                total_games += 1
                if team == game[2]:
                    if game[0] not in team_names:
                        total_top_25 -= 1
                        # print(team, game[0], full_team_names[game[0]])
                        upsets += 1
                    elif full_team_names[game[0]] > full_team_names[game[2]]:
                        upsets += 1
                        top_25 += 1
    else:
        total_games = 0
        total_top_25 = 0
        upsets = 0
        top_25 = 0
        for team in team_names:
            for game in team_games[team]:
                total_games += 1
                total_top_25 += 1
                if team == game[2]:
                    if game[0] not in team_names:
                        upsets += 1
                        total_top_25 -= 1
                    elif team_names[game[2]] > team_names[game[0]]:
                        upsets += 1
                        top_25 += 1
    return [upsets, upsets / total_games, top_25, top_25 / total_top_25]

def playoffs(rankings, records, postseason):
    playoff_upsets = [0]*len(rankings)
    tmp = 0
    for ranking in rankings:
        team_names = {records[ranking[j]][0]: j for j in range(len(ranking))}
        total = 0
        for game in postseason:
            if team_names[game[0]] < team_names[game[2]]:
                total += 1
        playoff_upsets[tmp] = total
        tmp += 1
    return playoff_upsets

def postseason_upsets(rankings, records, postseason):
    playoff_upsets = [0]*len(rankings)
    playoff_upsets_ratio = [0]*len(rankings)
    tmp = 0
    for ranking in rankings:
        team_names = {records[ranking[j]][0]: j for j in range(len(ranking))}
        week = 14
        discount = 1
        total = 0
        games_played = 0
        for game in postseason:
            if game[-1] > week:
                week = game[-1]
            if game[0] in team_names.keys() and game[2] not in team_names.keys() and game[1] <= game[3]:
                games_played += 1
                total += discount
            if game[2] in team_names.keys() and game[0] not in team_names.keys() and game[3] <= game[1]:
                games_played += 1
                total += discount
            if game[0] in team_names.keys() and game[2] in team_names.keys():
                games_played += 1
                if team_names[game[0]] < team_names[game[2]]:
                    total += discount
        playoff_upsets[tmp] = total
        if games_played != 0:
            playoff_upsets_ratio[tmp] = total / len(postseason)
        else:
            playoff_upsets_ratio[tmp] = 1
            playoff_upsets[tmp] = len(postseason)
        tmp += 1
    return playoff_upsets, playoff_upsets_ratio

def upsets(rankings, records, team_games, long_rankings, r_ap):
    upsets = [0] * len(rankings)
    for r in range(len(rankings)):
        upsets[r] = helper(rankings[r], records, team_games, long_rankings[r])
    upsets.append(helper(r_ap, records, team_games))
    return upsets

def statistical(dict):
    p_values = []
    for i in range(len(dict)-1):
        t_stat, p_value = ttest_rel(dict[i], dict[7])
        p_values.append(p_value)
    return p_values

