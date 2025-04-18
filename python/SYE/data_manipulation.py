# this is the file that holds all the functions related to reading in the NCAA
# generating the games array, team_games dictionary, and records array.
# as well as filtering out all the teams we don't want
import csv
from collections import defaultdict
from os import path
import re
from scraping import get_college_football_rankings

def remove_ranking(team_name):
    # some teams in this database are presented like (21) Notre Dame, and I'd rather remove that (21)
    # this will make it easier to query NCAA later
    if team_name[0] == '(':
      while team_name[0] != ' ':
        team_name = team_name.replace(team_name[0], '')
      team_name = team_name.replace(team_name[0], '')
    team_name = team_name.replace(' ', '')
    return team_name

def parse_game_data(game_str, extra_time):
    # Strip the string to remove any trailing commas or spaces

    game_str = game_str.replace('"', "")
    game_str = game_str.replace('&nbsp', '')
    game_str = game_str.strip()
    # Split the string by commas
    data_fields = game_str.split(',')

    # Convert the resulting list into a tuple
    game_tuple = tuple(data_fields)
    if game_tuple[0] == 'Rk' or game_tuple[0] == '' or game_tuple[-1] == 'Game Cancelled':
        return None
    if extra_time:
        game_tuple = (game_tuple[6], game_tuple[7], game_tuple[9], game_tuple[10], game_tuple[1])
    else:
        game_tuple = (game_tuple[5], game_tuple[6], game_tuple[8], game_tuple[9], game_tuple[1])
    win_team = remove_ranking(game_tuple[0])
    lose_team = remove_ranking(game_tuple[2])

    mislabeled = {'BrighamYoung':'BYU', 'MiamiFL':'Miami', 'SouthernMethodist':'SMU', 'LouisianaState':'LSU',
                  'NorthCarolinaState':'NCState', 'SouthernCalifornia':'USC', 'TexasChristian':'TCU', 'CentralFlorida':'UCF',
                  'Nevada-LasVegas':'UNLV', 'SouthernMississippi':'SouthernMiss'}

    if win_team in mislabeled.keys():
        win_team = mislabeled[win_team]
    if lose_team in mislabeled.keys():
        lose_team = mislabeled[lose_team]

    final = (win_team, game_tuple[1], lose_team, game_tuple[3], int(game_tuple[4]))
    return final

def parse_nfl_data(game_str):
    data_fields = game_str.split(',')
    # Convert the resulting list into a tuple
    game_tuple = tuple(data_fields)
    return game_tuple

def split_postseason(games):
    train = []
    test = []
    max_weeks = games[-1][-1]
    for game in games:
        if game[-1] <= max_weeks-4:
            train.append(game)
        else:
            test.append(game)
    return train, test

def split_rows(file_path):
    'NCAA/{year}.txt'
    league = file_path[0:3]
    if league == 'NFL':
        year = int(file_path[4:8])
    else: year = int(file_path[5:9])
    extra_time = False
    if year > 2012:
        extra_time = True

    # Split the rows by newline
    with open(file_path, 'r') as data:
        rows = data.read().strip().split("\n")
    # Create a list to hold all game NCAA as tuples
    games = []
    postseason = []

    if league == 'NCA':
        # Loop through each row
        for row in rows:
            # Split each row by commas
            data = parse_game_data(row, extra_time)
            if data is not None:
                games.append(data)
        return games
    if league == 'NFL':
        for row in rows:
            data_fields = row.split(',')
            # Convert the resulting list into a tuple
            data = tuple(data_fields)
            if data is not None:
                if data[-1] == 'REG':
                    games.append(data[:4])
                else:
                    postseason.append(data[:4])
        return games, postseason

def generate_dictionary(games):
    # Create a dictionary to store each team's games
    team_games = {}

    # Iterate over each game
    for game in games:
        # Extract the team (fifth field) and the game tuple
        winner = game[0]

        loser = game[2]

        # If the team is not in the dictionary, initialize a new list
        if winner not in team_games:

            team_games[winner] = []
        if loser not in team_games:
            team_games[loser] = []
        # Add the current game to the team's list
        team_games[winner].append(game)
        team_games[loser].append(game)
    return team_games

def generate_records(team_games):
    records = []
    for team, matches in team_games.items():
        wins = 0
        losses = 0
        ties = 0
        for time in matches:
            if (time[0] == team or time[2] == team) and time[1] == time[3]:
                ties += 1
            elif time[0] == team:
                wins += 1
            else:
                losses += 1
            ratio = wins / (wins + losses + ties)
        total = losses + wins + ties
        g = [team, wins, losses, ratio, total, ties]
        records.append(g)
    return records

def filter_teams(games, team_games, records):
    tmp = 0
    while tmp != len(records):
        tmp = len(records)
        for team in records:
            if team[4] < 4 or team[1] == 0:
                for game in games:
                    if game in team_games[team[0]]:
                        games.remove(game)
                del team_games[team[0]]
                records.remove(team)
        team_games = generate_dictionary(games)
        records = generate_records(team_games)
    return games, team_games, records

def generate_data(file_path, verbose=False, filter = True):
    # the massive array of all the games tuples
    league = file_path[0:3]
    postseason = None
    if league == 'NCA':
        games = split_rows(file_path)

    elif league == 'NFL':
        filter = False
        games, postseason = split_rows(file_path)

    # a dictionary of game info
    # Key: team name
    # Value: every tuple of games that they played in
    team_games = generate_dictionary(games)

    # an array of teams with tuples of stats
    # (name, wins, losses, ratio, total_games_played, ties)
    records = generate_records(team_games)
    if filter:
        tmp = 0
        while len(records) != tmp:
            tmp = len(records)
            games, team_games, records = filter_teams(games, team_games, records)
        if verbose:
            print(f"remaining teams post-filter: {tmp}")

    if league == 'NCA':
        games, postseason = split_postseason(games)

    # we have to remake our dictionary based on our shorter games array
    team_games = generate_dictionary(games)
    records = generate_records(team_games)

    return games, team_games, records, postseason

def try_load_rankings_from_csv(file_name, length):
    rankings = {f"Method_{i+1}": [None] * length for i in range(7)}  # Assuming max rank 130
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            year, method, rank, team = row
            rank = int(rank)
            team = int(team)
            rankings[method][rank - 1] = team  # Index by rank (0-based)
    return [rankings[f"Method_{i+1}"] for i in range(7)]

def load_rankings_from_csv(file_name):
    """
    Loads team rankings from a CSV file and returns a list of method-based rankings.
    Automatically detects the maximum rank length.

    Parameters:
    - file_name (str): Path to the CSV file

    Returns:
    - list of lists: rankings for Method_1 through Method_7
    """
    rankings = defaultdict(dict)  # {method: {rank: team}}
    max_rank = 0

    with open(file_name, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        for row in reader:
            if len(row) < 4:
                continue  # Skip invalid lines

            year, method, rank, team = row
            try:
                rank = int(rank)
                team = int(team)
                rankings[method][rank - 1] = team
                max_rank = max(max_rank, rank)
            except ValueError:
                continue  # Skip lines with invalid data

    # Construct final list of lists, ordered by Method_1 to Method_7
    return [
        [rankings.get(f"Method_{i+1}", {}).get(r, None) for r in range(max_rank)]
        for i in range(7)
    ]

def clean_team_name(raw_name):
    # This removes anything from the first "(" onward
    return re.sub(r"\s*\(.*?\)", "", raw_name).strip()

def get_ap_rankings(file_path, records):
    if not path.exists(file_path):
        return
    raw_teams = [line.strip().replace(' ', "") for line in open(file_path)]
    teams = [clean_team_name(team) for team in raw_teams]
    ranking_indices = []
    for team in teams:
        for i in range(len(records)):
            if team == records[i][0]:
                ranking_indices.append(i)
                break
    return teams, ranking_indices