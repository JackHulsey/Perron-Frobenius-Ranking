import csv
from os import path

import numpy as np

from data_manipulation import generate_data
from matrices.build_matrices import build_matrices
from matrix_math import fixed_point, linear_strengths, nonlinear_strengths, \
    inverse_power_method, make_B_matrix, inverse_power_method_two, solver, solver2, solver3, tournament, modern
from scraping import scrape_cfb_schedule, get_college_football_rankings


def output(ranking, records, limit=100, strength=None, reverse=False):
    if strength:
        strength = np.array(strength)
        s = np.argsort(-strength)
    else:
        ranking = np.array(ranking)
        if reverse:
            s = np.argsort(ranking)
        else:
            s = np.argsort(-ranking)
    iter = 1
    tmp = s[0]
    for num in s:
        if strength is not None:
            # output with strengths
            print(f"{iter:<3} {records[num][0]:<20} {round(strength[num], 6):<10} {round(strength[tmp] - strength[num], 5)}")
        else:
            # output with records of win-loss-tie
            if reverse:
                diff = ranking[num]-ranking[s[0]]
            else:
                diff = ranking[s[0]]-ranking[num]
            record = str(records[num][1]) + '-' + str(records[num][2]) + '-' + str(records[num][5])
            print(f"{iter:<3} {records[num][0]:<20} {record:<10} {ranking[num]:<25} {diff}")
        if iter == limit:
            return
        iter += 1
        tmp = num

def method_one(weighted_score_matrix, score_matrix, records, verbose = False):
    matrices = np.array(weighted_score_matrix)
    ranking, iter, every_rank = fixed_point(matrices, records)
    if verbose:
        print("\nMethod one: simple linear method using fixed point integrals to determine eigenvectors:")
        print(f"Iterations of fixed point integral: {iter}")
        strengths = linear_strengths(score_matrix, ranking, records)
        output(ranking, records, limit=len(records), strength=strengths)
    return np.argsort(np.array(-ranking))

def method_two(results_matrix, raw_score_matrix, score_matrix, records, verbose = False):
    ranking, iter, every_rank = nonlinear_strengths(raw_score_matrix, records)
    ranking = np.array(ranking)
    if verbose:
        print("\n\nMethod two: non-linear method using using strength of schedule")
        print(f"iterations of function F: {iter}")
        output(ranking, records, 40)
    return np.argsort(-np.array(ranking))

def method_three(raw_score_matrix, score_matrix, records, verbose = False):
    B = make_B_matrix(records, raw_score_matrix)
    B = np.array(B)

    ranking, iter = inverse_power_method(B)
    if verbose:
        print("\n\nMethod three: probabilistic approach of approximating pi_ij as the probability of i beating j")
        print(f"iterations of F: {iter}")
        #strengths = linear_strengths(score_matrix, ranking, records)
        output(ranking, records, 40, reverse=True)
    return np.argsort(np.array(ranking))

def method_four(A_matrix, records, verbose=False):
    ranking = solver3(A_matrix)
    if verbose:
        print("\n\nMethod four: the maximum likelihood method (Bradley-Terry model)")
        output(ranking, records, reverse=True, limit=40)
    return np.argsort(np.array(ranking))

def method_five(raw_matrix, records, verbose=False):
    ranking = tournament(raw_matrix)
    if verbose:
        print("\n\nMethod five: a graph theory perspective using tournaments")
        output(ranking, records, reverse=True, limit=40)
    return np.argsort(np.array(ranking))

def method_six(matrix, records, verbose=False):
    ranking = modern(matrix)
    if verbose:
        print("\n\nMethod six: taking a modern approach with scipy.linalg.eig")
        output(ranking, records, limit=len(records), reverse=True)
    # TODO: fix this so that the ranking outputs reversed when it needs to be
    ranking = np.argsort(np.array(ranking))
    if records[ranking[0]][1] < records[ranking[-1]][1]:
        print(records[ranking[0]])
        return ranking[::-1]
    return ranking

def convert(r, records):
    team_rankings = []
    for num in r:
        team_rankings.append(records[num][0])
    return team_rankings

def comparison(r_1, r_2, r_3, r_4, r_5, r_6, r_7, r_ap, records):
    r_1 = convert(r_1, records)
    r_2 = convert(r_2, records)
    r_3 = convert(r_3, records)
    r_4 = convert(r_4, records)
    r_5 = convert(r_5, records)
    r_6 = convert(r_6, records)
    r_7 = convert(r_7, records)

    print(f"Rank AP Poll         Linear          Nonlinear       Least Square    MLE             Tournaments     Modern          NFL Power")
    for i in range(len(r_ap)):
        print(f"{i+1:<4} {r_ap[i]:<15} {r_1[i]:<15} {r_2[i]:<15} {r_3[i]:<15} {r_4[i]:<15} {r_5[i]:<15} {r_6[i]:<15} {r_7[i]:<15}")

def generate_rankings(years, league):
    for year in years:
        if year == 2020:
            continue
        print(f"Evaluations from {year}:")
        # Check if the file already exists
        if not path.exists(f"NCAA/{year}.txt"):
            success = scrape_cfb_schedule(year)
        else:
            success = True

        if success:
            games, team_games, records, postseason = generate_data(f'{league}/{year}.txt')
            # build the five matrices we 'need'
            results_matrix, weighted_results_matrix, score_matrix, weighted_score_matrix, raw_score_matrix, A_matrix = build_matrices(team_games, records)

            ranking_one = method_one(weighted_score_matrix, score_matrix, records)
            ranking_two = method_two(results_matrix, raw_score_matrix, score_matrix, records)
            ranking_three = method_three(raw_score_matrix, score_matrix, records)
            ranking_four = method_four(A_matrix, records)
            ranking_five = method_five(raw_score_matrix, records)
            ranking_six = method_six(results_matrix, records)
            ranking_seven = nfl_power_rankings(games, records)

            rankings = [ranking_one, ranking_two, ranking_three, ranking_four, ranking_five, ranking_six, ranking_seven]
            rankings_data = []

            # Save rankings NCAA for later analysis
            for method_idx, ranking in enumerate(rankings, start=1):
                for rank, team in enumerate(ranking, start=1):
                    rankings_data.append([year, f"Method_{method_idx}", rank, team])

            # Write rankings to a CSV file for the specific year
            file_name = f"rankings/{league}/rankings_{year}.csv"
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Year", "Method", "Rank", "Team"])
                writer.writerows(rankings_data)

            print(f"Rankings for {year} have been saved to {file_name}")

# Define ELO update function
def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def nfl_power_rankings(games, records):
    team_names = {records[i][0]: i for i in range(len(records))}
    # ELO settings
    Base_elo = 1500
    k = 32
    elo = {team: Base_elo for team in team_names}

    def update_elo(game, K):
        ea = expected_score(elo[game[0]], elo[game[2]])
        eb = expected_score(elo[game[2]], elo[game[0]])

        if game[1] > game[3]:
            sa, sb = 1, 0
        elif game[1] < game[3]:
            sa, sb = 0, 1
        else:
            sa, sb = 0.5, 0.5  # Tie

        elo[game[0]] += K * (sa - ea)
        elo[game[2]] += K * (sb - eb)

    for game in games:
        update_elo(game, k)

    sorted_dict = sorted(elo.items(), key=lambda x: x[1], reverse=True)
    rankings = []
    for team, elo in sorted_dict:
        rankings.append(elo)
    rankings = np.argsort(np.array(rankings))
    return rankings

