import numpy as np

# contains the function to calculate the entries for a matrix

# Simply returns a 1 or a 0 for win or loss 0.5 for tie
def match_result(team_games, team_i, team_j):

    # a_ij
    # 0: team_i wins, 1: team_j wins, 0.5: tie
    played = team_games[team_i]
    for game in played:
      if game[0] == team_i and game[2] == team_j:
        if game[1] == game[3]:
          return 0.5
        return 1
      if game[1] == team_j and game[3] == team_i:
        if game[1] == game[3]:
          return 0.5
        return 0
    return 0

# Returns the same 1, 0, 0.5 but divides it by the number of games that team played
def match_result_weighted(team_games, team_i, team_j, num_game):
    # a_ij / n_i
    played = team_games[team_i]
    for game in played:
      if game[0] == team_i and game[2] == team_j:
        if game[1] == game[3]:
          return round(0.5 / num_game, 5)
        return round(1 / num_game, 5)
      if game[0] == team_j and game[2] == team_i:
        if game[1] == game[3]:
          return round(0.5 / num_game, 5)
        return 0
    return 0

# score of the team, one team on one half of the matrix the other on the second half
def raw_match_score(team_games, team_i, team_j):
    played = team_games[team_i]
    for game in played:
      if game[0] == team_i and game[2] == team_j:
        return int(game[1])
      if game[0] == team_j and game[2] == team_i:
        return int(game[3])
    return 0

# helper functions
def h(x):
  result = 0.5 + 0.5*np.sign(x - 0.5)*np.sqrt(abs(2*x -1))
  return result

def score(s1, s2):
  return h(float((s1 + 1) / (s1 + s2 + 2)))

# calculating the proportion of the scores using helper functions
def match_score(team_games, team_i, team_j):
    # 0: team_i wins, 1: team_j wins, 0.5: tie
    played = team_games[team_i]
    for game in played:
      if game[0] == team_i and game[2] == team_j:
        return score(float(game[1]), float(game[3]))
      if game[0] == team_j and game[2] == team_i:
        return score(float(game[3]), float(game[1]))
    return 0

# same as the match score but divided by the number of games
def weight_match_score(team_games, team_i, team_j, num_games):
    # 0: team_i wins, 1: team_j wins, 0.5: tie
    played = team_games[team_i]
    for game in played:
      if game[0] == team_i and game[2] == team_j:
        return score(float(game[1]), float(game[3])) / num_games
      if game[0] == team_j and game[2] == team_i:
        return score(float(game[3]), float(game[1])) / num_games
    return 0

# 1 if win 0 otherwise
def binary_result(team_games, team_i, team_j):
    # Simply returns a 1 or a 0 for win or loss 0.5 for tie
    # a_ij
    # 0: team_i wins, 1: team_j wins, 0.5: tie
    played = team_games[team_i]
    for game in played:
      if game[0] == team_i and game[2] == team_j:
        if game[1] == game[3]:
          return 0
        return 1
      if game[0] == team_j and game[2] == team_i:
        if game[1] == game[3]:
          return 0
        return 0
    return 0

# a_ij = S_ij / (S_ij + S_ji)
def proportions(team_games, team_i, team_j):
    played = team_games[team_i]
    for game in played:
        if game[1] == '0' and game[3] == '0':
            return 0
        if game[0] == team_i and game[2] == team_j:
            return int(game[1]) / (int(game[1]) + int(game[3]))
        if game[0] == team_j and game[2] == team_i:
            return int(game[3]) / (int(game[3]) + int(game[1]))
    return 0

