# main file for actually running the program
import csv

import numpy as np
from os import path

from Evaluations import compare_rankings, upsets
from matrices.build_matrices import build_matrices
from data_manipulation import generate_data

from ranking import method_one, method_two, method_three, method_four, method_five, method_six, comparison, \
    generate_rankings
from scraping import scrape_cfb_schedule, get_college_football_rankings
from testing import count_inversions, load_rankings_from_csv


def main():
    # initalize data
    years = [1978 + i for i in range(47)]
    ndcg_dict = {i:[] for i in range(6)}
    num_upsets = {i:[] for i in range(7)}
    ratio_upsets = {i:[] for i in range(7)}
    inv_dict = {i:[] for i in range(6)}
    top_25_dict = {i:[] for i in range(7)}
    top_25_ratio = {i:[] for i in range(7)}
    # generate_rankings(years)

    for year in years:
        if year == 2020:
            continue
        # print(f"Evaluations from {year}:")
        # Check if the file already exists
        if not path.exists(f"data/{year}.txt"):
            success = scrape_cfb_schedule(year)
        else:
            success = True

        if success:
            games, team_games, records = generate_data(f'data/{year}.txt')
            ap_rankings, ap_indices = get_college_football_rankings(year, records)

            # comparison(ranking_one, ranking_two, ranking_three, ranking_four, ranking_five, ranking_six, ap_rankings, records)
            # print(len(records))
            rankings = load_rankings_from_csv(f'rankings/rankings_{year}.csv', len(records))
            shorter_rankings = [r[:25] for r in rankings]
            # shorter_rankings = [ranking_one[:25], ranking_two[:25], ranking_three[:25], ranking_four[:25], ranking_five[:25], ranking_six[:25]]
            ideal, ndcg = compare_rankings(ap_indices, shorter_rankings)
            upset = upsets(shorter_rankings, records, team_games, rankings, ap_indices)
            inversion_counts = [count_inversions(shorter_rankings[i], ap_indices) for i in range(len(shorter_rankings))]


            for i in range(len(rankings)):
                inv_dict[i].append(inversion_counts[i])
                ndcg_dict[i].append(ndcg[i])
                num_upsets[i].append(upset[i][0])
                ratio_upsets[i].append(upset[i][1])
                top_25_dict[i].append(upset[i][2])
                top_25_ratio[i].append(upset[i][3])
                # print(f"{year} | Method_{i+1}: | ndcg: {round(float(ndcg[i]), 5):<7} |  number of upsets: {upset[i][0]:<4} | ratio: {round(upset[i][1], 4):<9} | Upsets Within top 25: {upset[i][2]:<4} | Upsets Within top 25 ratio: {upset[i][3]:<4}")
            num_upsets[6].append(upset[-1][0])
            ratio_upsets[6].append(upset[-1][1])
            top_25_dict[6].append(upset[-1][2])
            top_25_ratio[6].append(upset[-1][3])
            # print(f"{year} | AP_Polls: | ndcg: {1:<7} |  number of upsets: {upset[-1][0]:<4} | ratio: {round(upset[-1][1], 4):<9} | Upsets Within top 25: {upset[-1][2]:<4} | Upsets Within top 25 ratio: {upset[-1][3]:<4}")


    print(f"{years[0]}-{years[-1]}")
    print(f"AP_Polls | avg_ndcg: {1.0:<5} | avg_upsets: {round(np.average(num_upsets[6]), 2):<6} | avg_ratio: {round(np.average(ratio_upsets[6]), 4):<6} | Upsets Within top 25: {round(np.average(top_25_dict[6]), 3):<4} | Upsets Within top 25 ratio: {round(np.average(top_25_ratio[6]), 4)}")
    for i in range(len(ndcg_dict)):
        print(f"Method_{i+1} | avg_ndcg: {round(np.average(ndcg_dict[i]), 2):<5} | avg_upsets: {round(np.average(num_upsets[i]), 3):<6} | avg_ratio: {round(np.average(ratio_upsets[i]), 4):<4} | Upsets Within top 25: {round(np.average(top_25_dict[i]), 3)} | Upsets Within top 25 ratio: {round(np.average(top_25_ratio[i]), 4)}")

if __name__ == '__main__':
    main()
