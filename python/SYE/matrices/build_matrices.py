import networkx as nx
from matplotlib import pyplot as plt

from matrices.calculate_entries import (match_result_weighted,
                                        weight_match_score, match_score,
                                        match_result, raw_match_score, proportions)


def make_results_matrix(team_games, records):
    # Initialize square matrix for results
    n = len(records)
    matrix = [[0] * n for _ in range(n)]

    # Fill the matrix with match result
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0  # A team doesn't play against itself
            else:
                # replace match_result() with any other function from calculate_entries.py
                matrix[i][j] = match_result(team_games, records[i][0], records[j][0])
    return matrix

def make_weighted_results_matrix(team_games, records):
    # Initialize square matrix for results
    n = len(records)
    matrix = [[0] * n for _ in range(n)]

    # Fill the matrix with match result
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0  # A team doesn't play against itself
            else:
                matrix[i][j] = match_result_weighted(team_games, records[i][0], records[j][0], records[i][4])
    return matrix

def make_score_matrix(team_games, records):
    # Initialize square matrix for results
    n = len(records)
    matrix = [[0] * n for _ in range(n)]

    # Fill the matrix with match result
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0  # A team doesn't play against itself
            else:
                matrix[i][j] = match_score(team_games, records[i][0], records[j][0])
    return matrix

def make_raw_score_matrix(team_games, records):
    # Initialize square matrix for results
    n = len(records)
    matrix = [[0] * n for _ in range(n)]

    # Fill the matrix with match result
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0  # A team doesn't play against itself
            else:
                matrix[i][j] = raw_match_score(team_games, records[i][0], records[j][0])
    return matrix

def make_weighted_score_matrix(team_games, records):
    # Initialize square matrix for results
    n = len(records)
    matrix = [[0] * n for _ in range(n)]

    # Fill the matrix with match result
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0  # A team doesn't play against itself
            else:
                matrix[i][j] = weight_match_score(team_games, records[i][0], records[j][0], records[i][4])
    return matrix

def make_A_matrix(team_games, records):
    # Initialize square matrix for results
    n = len(records)
    matrix = [[0] * n for _ in range(n)]

    # Fill the matrix with match result
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0  # A team doesn't play against itself
            else:
                matrix[i][j] = proportions(team_games, records[i][0], records[j][0])
    return matrix


def draw_digraph_from_matrix(matrix, labels=None):
    """
    Generates a directed graph from an adjacency matrix.

    Parameters:
    - matrix (list of list or np.array): Adjacency matrix representing the digraph.
    - labels (list, optional): Labels for the nodes. Defaults to numeric indices.
    """
    G = nx.DiGraph()

    n = len(matrix)
    if labels is None:
        labels = list(range(n))

    # Add nodes
    for i in range(n):
        G.add_node(labels[i])

    # Add edges
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                G.add_edge(labels[i], labels[j], weight=matrix[i][j])

    pos = nx.spring_layout(G, k=3.5, seed=44)  # consistent layout
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, arrows=True, node_color='#009CDE', edge_color="gray", node_size=100, font_size=10)
    plt.title("Directed Graph from Adjacency Matrix")
    plt.axis("off")
    plt.show()






def build_matrices(team_games, records):
    results_matrix = make_results_matrix(team_games, records)
    weighted_results_matrix = make_weighted_results_matrix(team_games, records)
    scores_matrix = make_score_matrix(team_games, records)
    weighted_scores_matrix = make_weighted_score_matrix(team_games, records)
    raw_scores_matrix = make_raw_score_matrix(team_games, records)
    A_matrix = make_A_matrix(team_games, records)
    draw_digraph_from_matrix(raw_scores_matrix)
    return results_matrix, weighted_results_matrix, scores_matrix, weighted_scores_matrix, raw_scores_matrix, A_matrix

