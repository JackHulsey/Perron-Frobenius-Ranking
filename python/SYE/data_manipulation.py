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

def parse_game_data(game_str):
    # Strip the string to remove any trailing commas or spaces
    game_str = game_str.strip()

    # Split the string by commas
    data_fields = game_str.split(',')

    # Convert the resulting list into a tuple
    game_tuple = tuple(data_fields)

    win_team = remove_ranking(game_tuple[4])
    lose_team = remove_ranking(game_tuple[7])

    final = (game_tuple[0], game_tuple[1], game_tuple[2], game_tuple[3], win_team,
                  game_tuple[5], lose_team, game_tuple[8], game_tuple[9])

    return final

def split_rows(file_path):
  # Split the rows by newline
    with open(file_path, 'r') as data:
        rows = data.read().strip().split("\n")
    # Create a list to hold all game data as tuples
    games = []

    # Loop through each row
    for row in rows:
        # Split each row by commas
         data = parse_game_data(row)
         games.append(data)
    return games

def generate_dictionary(games):
    # Create a dictionary to store each team's games
    team_games = {}

    # Iterate over each game
    for game in games:
        # Extract the team (fifth field) and the game tuple
        winner = game[4]
        loser = game[6]

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
            if (time[4] == team or time[6] == team) and time[5] == time[7]:
                ties += 1
            elif time[4] == team:
                wins += 1
            else:
                losses += 1
            ratio = wins / (wins + losses + ties)
        total = losses + wins + ties
        g = [team, wins, losses, ratio, total, ties]
        records.append(g)
    return records

def filter_teams(games, team_games, records):
    for team in records:
        if team[4] < 3 or team[1] == 0:
            for game in games:
                if game in team_games[team[0]]:
                    games.remove(game)
            del team_games[team[0]]
            records.remove(team)
    return games, team_games, records

def generate_data(file_path):
    # the massive array of all the games tuples
    games = split_rows(file_path)

    # a dictionary of game info
    # Key: team name
    # Value: every tuple of games that they played in
    team_games = generate_dictionary(games)
    # an array of teams with tuples of stats
    # (name, wins, losses, ratio, total_games_played, ties)
    records = generate_records(team_games)

    tmp = 0
    while len(records) != tmp:
        tmp = len(records)
        games, team_games, records = filter_teams(games, team_games, records)
        print(tmp)
    # we have to remake our dictionary based on our shorter games array
    team_games = generate_dictionary(games)
    # print(len(records))

    return games, team_games, records
