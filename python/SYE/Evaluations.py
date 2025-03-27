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
    Calculate Discounted Cumulative Gain at rank k for a given ranking and relevance scores.

    ranking: List of indices representing the ranking.
    relevance_scores: List of relevance scores corresponding to the items in the ranking.
    k: Rank at which to calculate DCG.

    Returns the DCG value.
    """
    dcg = 0
    for i in range(min(k, len(ranking))):
        rank_pos = ranking[i]  # Item at the i-th position
        dcg += relevance_scores[rank_pos] / np.log2(i + 2)  # +2 because we want log(i+1) with i starting at 0
    return dcg


def ndcg_at_k(ranking, relevance_scores, ideal_ranking, ideal_relevance_scores, k):
    """
    Calculate Normalized Discounted Cumulative Gain at rank k.

    ranking: List of indices representing the ranking to evaluate.
    relevance_scores: List of relevance scores corresponding to the items in the ranking.
    ideal_ranking: List of indices representing the ideal ranking.
    ideal_relevance_scores: List of relevance scores corresponding to the ideal ranking.
    k: Rank at which to calculate NDCG.

    Returns the NDCG value.
    """
    dcg = dcg_at_k(ranking, relevance_scores, k)
    idcg = dcg_at_k(ideal_ranking, ideal_relevance_scores, k)
    return dcg / idcg if idcg != 0 else 0


def compare_rankings(ranking1, ranking2):
    """
    Compare two rankings using NDCG, where relevance scores are based on rank positions.

    ranking1: First ranking to evaluate.
    ranking2: Second ranking to evaluate.
    num_items: Total number of items (for generating relevance scores).
    k: Rank at which to calculate NDCG.

    Returns the NDCG values for both rankings.
    """
    num_items = len(ranking1)
    k = num_items
    # Relevance scores based on rank positions: lower rank means higher relevance
    relevance_scores = np.array([1 / (i + 1) for i in range(num_items)])  # Exponential decay, e.g. 1, 0.5, 0.33, ...

    # Ideal ranking is the ranking of the items based on the true relevance scores (highest relevance first)
    ideal_ranking = sorted(range(len(relevance_scores)), key=lambda x: relevance_scores[x], reverse=True)
    ideal_relevance_scores = [relevance_scores[i] for i in ideal_ranking]

    # Calculate NDCG for both rankings
    ndcg1 = ndcg_at_k(ranking1, relevance_scores, ideal_ranking, ideal_relevance_scores, k)
    ndcg2 = ndcg_at_k(ranking2, relevance_scores, ideal_ranking, ideal_relevance_scores, k)

    return ndcg1, ndcg2