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

def build_matrices(team_games, records):
    results_matrix = make_results_matrix(team_games, records)
    weighted_results_matrix = make_weighted_results_matrix(team_games, records)
    scores_matrix = make_score_matrix(team_games, records)
    weighted_scores_matrix = make_weighted_score_matrix(team_games, records)
    raw_scores_matrix = make_raw_score_matrix(team_games, records)
    A_matrix = make_A_matrix(team_games, records)
    return results_matrix, weighted_results_matrix, scores_matrix, weighted_scores_matrix, raw_scores_matrix, A_matrix

