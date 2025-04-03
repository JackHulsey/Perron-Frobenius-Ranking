# main file for actually running the program
import numpy as np
from os import path

from Evaluations import compare_rankings, upsets
from matrices.build_matrices import build_matrices
from data_manipulation import generate_data

from ranking import method_one, method_two, method_three, method_four, method_five, method_six, comparison
from scraping import scrape_cfb_schedule, get_college_football_rankings
from testing import count_inversions


def main():
    # initalize data
    years = [2021 + i for i in range(1)]
    ndcg_dict = {i:[] for i in range(6)}
    num_upsets = {i:[] for i in range(6)}
    ratio_upsets = {i:[] for i in range(6)}
    inv_dict = {i:[] for i in range(6)}
    for year in years:
        print(f"Evaluations from {year}:")
        # Check if the file already exists
        if not path.exists(f"data/{year}.txt"):
            success = scrape_cfb_schedule(year)
        else:
            success = True

        if success:
            games, team_games, records = generate_data(f'data/{year}.txt')
            ap_rankings, ap_indices = get_college_football_rankings(year, records)
            #print(games)
            # build the five matrices we 'need'
            results_matrix, weighted_results_matrix, score_matrix, weighted_score_matrix, raw_score_matrix, A_matrix = build_matrices(team_games, records)

            ranking_one = method_one(weighted_score_matrix, score_matrix, records)
            ranking_two = method_two(results_matrix, raw_score_matrix, score_matrix, records)
            ranking_three = method_three(raw_score_matrix, score_matrix, records)
            ranking_four = method_four(A_matrix, records)
            ranking_five = method_five(raw_score_matrix, records)
            ranking_six = method_six(weighted_score_matrix, records)

            # comparison(ranking_one, ranking_two, ranking_three, ranking_four, ranking_five, ranking_six, ap_rankings, records)

            # print(kendall_tau(ap_rankings, ranking_one[:25]))

            rankings = [ranking_one, ranking_two, ranking_three, ranking_four, ranking_five, ranking_six]
            shorter_rankings = [ranking_one[:25], ranking_two[:25], ranking_three[:25], ranking_four[:25], ranking_five[:25], ranking_six[:25]]
            ideal, ndcg = compare_rankings(ap_indices, shorter_rankings)
            upset = upsets(shorter_rankings, records, team_games)
            #print(upset)
            inversion_counts = [count_inversions(shorter_rankings[i], ap_indices) for i in range(len(shorter_rankings))]


            for i in range(len(rankings)):
                inv_dict[i].append(inversion_counts[i])
                ndcg_dict[i].append(ndcg[i])
                num_upsets[i].append(upset[i][0])
                ratio_upsets[i].append(upset[i][1])
                print(f"{year} | Method_{i+1}: | ndcg: {round(float(ndcg[i]), 5):<7} |  number of upsets: {upset[i][0]:<4} | ratio: {round(upset[i][1], 4):<9} | inversions: {inversion_counts[i]}")
    for i in range(len(ndcg_dict)):
        print(f"Method_{i+1} | avg_ndcg: {round(np.average(ndcg_dict[i]), 4)} | avg_upsets: {np.average(num_upsets[i])} | avg_ratio: {round(np.average(ratio_upsets[i]), 4)} | inversions: {np.average(inv_dict[i])}")
if __name__ == '__main__':
    main()
