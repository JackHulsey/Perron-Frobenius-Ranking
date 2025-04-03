import numpy as np

def kendall_tau(rank1, rank2):
    # Ensure that both ranks have the same length
    if len(rank1) != len(rank2):
        raise ValueError("The rankings must have the same length.")

    # Count concordant and discordant pairs
    concordant = 0
    discordant = 0
    n = len(rank1)

    # Compare each pair of items
    for i in range(n):
        for j in range(i + 1, n):
            if (rank1[i] < rank1[j] and rank2[i] < rank2[j]) or (rank1[i] > rank1[j] and rank2[i] > rank2[j]):
                concordant += 1
            elif (rank1[i] < rank1[j] and rank2[i] > rank2[j]) or (rank1[i] > rank1[j] and rank2[i] < rank2[j]):
                discordant += 1

    # Calculate Kendall's Tau
    tau = (concordant - discordant) / (n * (n - 1) / 2)

    return tau


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
    ndcg_scores = [ndcg(r_ap, r) / ideal for r in rankings]

    return ideal, ndcg_scores

def helper(ranking, records, team_games):
    team_names = {records[ranking[j]][0]: j for j in range(len(ranking))}
    upsets = 0
    upsets_ratio = 0
    weighted_count = 0

    for team in team_games:
        for game in team_games[team]:
            if team == game[2] and team_names[game[0]] > team_names[game[2]]:
                upsets += 1
                upsets_ratio += ((team_names[game[0]] + 1) / (team_names[game[2]] + 1))
                weighted_count += 1 / (team_names[game[2]] + 1)

    return [upsets, upsets_ratio, weighted_count]

def upsets(rankings, records, team_games):
    upsets = [0] * len(rankings)
    for r in range(len(rankings)):
        upsets[r] = helper(rankings[r], records, team_games)
    return upsets