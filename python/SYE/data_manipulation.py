# this is the file that holds all the functions related to reading in the data
# generating the games array, team_games dictionary, and records array.
# as well as filtering out all the teams we don't want

def remove_ranking(team_name):
    # some teams in this database are presented like (21) Notre Dame, and I'd rather remove that (21)
    # this will make it easier to query data later
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
        game_tuple = (game_tuple[6], game_tuple[7], game_tuple[9], game_tuple[10])
    else:
        game_tuple = (game_tuple[5], game_tuple[6], game_tuple[8], game_tuple[9])
    win_team = remove_ranking(game_tuple[0])
    lose_team = remove_ranking(game_tuple[2])

    mislabeled = {'BrighamYoung':'BYU', 'MiamiFL':'Miami', 'SouthernMethodist':'SMU', 'LouisianaState':'LSU',
                  'NorthCarolinaState':'NCState', 'SouthernCalifornia':'USC', 'TexasChristian':'TCU', 'CentralFlorida':'UCF',
                  'Nevada-LasVegas':'UNLV', 'SouthernMississippi':'SouthernMiss'}

    if win_team in mislabeled.keys():
        win_team = mislabeled[win_team]
    if lose_team in mislabeled.keys():
        lose_team = mislabeled[lose_team]

    final = (win_team, game_tuple[1], lose_team, game_tuple[3])
    return final

def split_rows(file_path):
    'data/{year}.txt'
    year = int(file_path[5:9])
    extra_time = False
    if year > 2012:
        extra_time = True

    # Split the rows by newline
    with open(file_path, 'r') as data:
        rows = data.read().strip().split("\n")
    # Create a list to hold all game data as tuples
    games = []

    # Loop through each row
    for row in rows:
        # Split each row by commas
        data = parse_game_data(row, extra_time)
        if data is not None:
            games.append(data)
    return games

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
    games = split_rows(file_path)

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
    # we have to remake our dictionary based on our shorter games array
    team_games = generate_dictionary(games)
    # print(len(records))

    return games, team_games, records