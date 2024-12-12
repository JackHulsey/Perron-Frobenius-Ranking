import numpy as np

# Simply returns a 1 or a 0 for win or loss 0.5 for tie
# a_ij
def match_result(team_games, team_i, team_j):
    # 0: team_i wins, 1: team_j wins, 0.5: tie
    played = team_games[team_i]
    for game in played:
      if game[4] == team_i and game[6] == team_j:
        if game[5] == game[7]:
          return 0.5
        return 1
      if game[5] == team_j and game[7] == team_i:
        if game[3] == game[5]:
          return 0.5
        return 0
    return 0

# Returns the same 1, 0, 0.5 but divides it by the number of games that team played
# a_ij / n_i
def match_result_weighted(team_games, team_i, team_j, num_game):
    # 0: team_i wins, 1: team_j wins, 0.5: tie
    played = team_games[team_i]
    for game in played:
      if game[4] == team_i and game[6] == team_j:
        if game[5] == game[7]:
          return round(0.5 / num_game, 5)
        return round(1 / num_game, 5)
      if game[5] == team_j and game[7] == team_i:
        if game[3] == game[5]:
          return round(0.5 / num_game, 5)
        return 0
    return 0

# subtracts the loser's score from the winners
def raw_match_score(team_games, team_i, team_j):
    # 0: team_i wins, 1: team_j wins, 0.5: tie
    played = team_games[team_i]
    for game in played:
      if game[4] == team_i and game[6] == team_j:
        return game[5] - game[7]
      if game[4] == team_j and game[6] == team_i:
        return game[5] - game[7]
    return 0

# helper functions to make 2.4 in the paper
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
      if game[4] == team_i and game[6] == team_j:
        return score(float(game[5]), float(game[7]))
      if game[4] == team_j and game[6] == team_i:
        return score(float(game[7]), float(game[5]))
    return 0

# same as the match score but divided by the number of games
def weight_match_score(team_games, team_i, team_j, num_games):
    # 0: team_i wins, 1: team_j wins, 0.5: tie
    played = team_games[team_i]
    for game in played:
      if game[4] == team_i and game[6] == team_j:
        return score(float(game[5]), float(game[7])) / num_games
      if game[4] == team_j and game[6] == team_i:
        return score(float(game[7]), float(game[5])) / num_games
    return 0