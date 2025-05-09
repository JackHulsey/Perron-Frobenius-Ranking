# main file for actually running the program
import csv

import numpy as np
from os import path

from scipy.stats import ttest_rel

from Evaluations import compare_rankings, upsets, playoffs, postseason_upsets, statistical
from data_manipulation import generate_data, load_rankings_from_csv, get_ap_rankings, try_load_rankings_from_csv
from ranking import generate_rankings, comparison
from scraping import scrape_cfb_schedule
from visualizations import plot_boxplot_upsets
from testing import plot_upsets_per_year, scatter_ndcg_vs_playoff_upsets, scatter_ndcg_vs_playoff_upsets_by_year, \
    plot_grouped_bar_avg_ndcg_ratio


def main():
    # initalize NCAA
    league = 'NCAA'
    years = [1978 + i for i in range(47)]
    if 2020 in years:
        years.remove(2020)
    num_rankings = 7
    ndcg_dict = {i:[] for i in range(num_rankings)}
    num_upsets = {i:[] for i in range(num_rankings+1)}
    ratio_upsets = {i:[] for i in range(num_rankings+1)}
    top_25_dict = {i:[] for i in range(num_rankings+1)}
    top_25_ratio = {i:[] for i in range(num_rankings+1)}
    playoff_upsets = {i:[] for i in range(num_rankings+1)}
    playoff_ratio = {i:[] for i in range(num_rankings+1)}
    # generate_rankings(years, 'NCAA')

    for year in years:
        # print(f"Evaluations from {year}:")
        # Check if the file already exists
        if not path.exists(f"NCAA/{year}.txt"):
            success = scrape_cfb_schedule(year)
        else:
            success = True

        if success:
            games, team_games, records, postseason = generate_data(f'{league}/{year}.txt')

            ap_rankings, ap_indices = get_ap_rankings(f'rankings/AP/Week_14/{year}.txt', records)
            coach_rankings, coach_indices = get_ap_rankings(f'rankings/Coaches/{year}.txt', records)
            print(len(ap_indices) == len(coach_indices))
            print(len(ap_indices), len(coach_indices))
            print(coach_indices[-1])
            rankings = load_rankings_from_csv(f'rankings/{league}/rankings_{year}.csv')
            shorter_rankings = [r[:len(ap_indices)] for r in rankings]
            ideal, ndcg = compare_rankings(ap_indices, shorter_rankings)
            upset = upsets(shorter_rankings, records, team_games, rankings, ap_indices)
            all_rankings = shorter_rankings
            all_rankings.append(ap_indices)
            # output_ranks_for_essay(all_rankings, rankings, records)
            # all_rankings.append(coach_indices)
            playoff_upset, ratio = postseason_upsets(all_rankings, records, postseason)
            # comparison(shorter_rankings[0], shorter_rankings[1], shorter_rankings[2], shorter_rankings[3], shorter_rankings[4], shorter_rankings[5], ap_rankings, records)
            for i in range(num_rankings):
                ndcg_dict[i].append(ndcg[i])
                num_upsets[i].append(upset[i][0])
                ratio_upsets[i].append(upset[i][1])
                top_25_dict[i].append(upset[i][2])
                top_25_ratio[i].append(upset[i][3])
                playoff_upsets[i].append(playoff_upset[i])
                playoff_ratio[i].append(1-ratio[i])
                print(f"{year} | Method_{i+1}: | ndcg: {round(float(ndcg[i]), 5):<7} |  number of upsets: {upset[i][0]:<4} | ratio: {round(upset[i][1], 4):<9} | Upsets Within top 25: {upset[i][2]} | Upsets Within top 25 ratio: {round(upset[i][3], 2)} | playoff upsets: {round(playoff_upset[i], 2)}")
            num_upsets[num_rankings].append(upset[-1][0])
            ratio_upsets[num_rankings].append(upset[-1][1])
            top_25_dict[num_rankings].append(upset[-1][2])
            top_25_ratio[num_rankings].append(upset[-1][3])
            playoff_upsets[num_rankings].append(playoff_upset[-1])
            playoff_ratio[num_rankings].append(1-ratio[-1])
            print(f"{year} | AP_Polls: | ndcg: {1:<7} |  number of upsets: {upset[-1][0]:<4} | ratio: {round(upset[-1][1], 4):<9} | Upsets Within top 25: {upset[-1][2]:<2} | Upsets Within top 25 ratio: {round(upset[-1][3], 3):<4} | playoff upsets: {round(playoff_upset[-1], 2)}")
    print(f"{years[0]}-{years[-1]}")
    print(f"AP_Polls | avg_ndcg: {1.0:<5} | avg_upsets: {round(np.average(num_upsets[num_rankings]), 2):<6} | avg_ratio: {round(np.average(ratio_upsets[num_rankings]), 4):<6} | Upsets Within top 25: {round(np.average(top_25_dict[num_rankings]), 3):<4} | Upsets Within top 25 ratio: {round(np.average(top_25_ratio[num_rankings]), 3)} | playoff upsets: {round(np.average(playoff_upsets[num_rankings]), 2)} | avg ratio: {round(np.average(playoff_ratio[num_rankings]), 2)} ")
    for i in range(len(ndcg_dict)):
        print(f"Method_{i+1} | avg_ndcg: {round(np.average(ndcg_dict[i]), 2):<5} | avg_upsets: {round(np.average(num_upsets[i]), 3):<6} | avg_ratio: {round(np.average(ratio_upsets[i]), 4):<4} | Upsets Within top 25: {round(np.average(top_25_dict[i]), 3)} | Upsets Within top 25 ratio: {round(np.average(top_25_ratio[i]), 4)} | playoff upsets: {round(np.average(playoff_upsets[i]), 2)} | avg ratio: {round(np.average(playoff_ratio[i]), 2)}")

    del ndcg_dict[6]
    del top_25_dict[6]
    del top_25_ratio[6]
    del playoff_upsets[6]
    del playoff_ratio[6]
    del num_upsets[6]

    plot_boxplot_upsets(num_upsets)
    plot_boxplot_upsets(top_25_dict, 'Top 25 Upsets')
    plot_boxplot_upsets(playoff_upsets)
    plot_boxplot_upsets(playoff_ratio, "Proportion of Games Correct", "Proportion of Games Correct")
    scatter_ndcg_vs_playoff_upsets_by_year('Method 4', ndcg_dict[5], playoff_ratio[5], years)
    plot_grouped_bar_avg_ndcg_ratio(ndcg_dict, playoff_ratio)
    print(statistical(playoff_upsets))
    print(statistical(playoff_ratio))
    print(statistical(top_25_dict))
    # comparison(shorter_rankings[0], shorter_rankings[1], shorter_rankings[2], shorter_rankings[3], shorter_rankings[4], shorter_rankings[5], shorter_rankings[6], ap_rankings, records)

def nfl():
    years = [1999 + i for i in range(1, 26)]
    num_rankings = 7
    upsets_dict = {i:[] for i in range(num_rankings)}
    prop_dict = {i:[] for i in range(num_rankings)}
    # generate_rankings(years, 'NFL')
    for year in years:
        if year == 2020:
            continue

        games, team_games, records, postseason = generate_data(f'NFL/{year}.txt')
        rankings = load_rankings_from_csv(f'rankings/NFL/rankings_{year}.csv')
        playoff_upsets = playoffs(rankings, records, postseason)
        for i in range(len(rankings)):
            upsets_dict[i].append(playoff_upsets[i])
            prop_dict[i].append(1 - (playoff_upsets[i] / len(postseason)))
            print(f"Method_{i+1} | Playoff upsets: {playoff_upsets[i]:<2} | ratio: {round(playoff_upsets[i] / len(postseason), 4):<9}")
        print(f"{year}")
    print(f"{years[0]}-{years[-1]}")
    for i in range(len(rankings)):
        print(f"Method_{i+1} | Playoff upsets: {round(np.average(upsets_dict[i]), 2)} | ratio: {round(np.average(playoff_upsets[i]) / len(postseason), 4):<9} ")
    plot_boxplot_upsets(upsets_dict)
    plot_boxplot_upsets(prop_dict)

def output_ranks_for_essay(rankings, long_rankings, records):
    team_dict = {i: records[i][0] for i in range(len(records))}
    num_teams = len(rankings[7])  # use one of the rankings as the reference

    for i in range(num_teams):
        team_id = rankings[7][i]
        team_name = team_dict.get(team_id, f"Unknown({team_id})")

        ranks = []
        for j in range(len(rankings)):
            ranking = rankings[j]
            if j != len(rankings)-1:
                fallback = long_rankings[j]

            if team_id in ranking:
                ranks.append(ranking.index(team_id) + 1)  # 1-based index
            elif team_id in fallback:
                ranks.append(f"{fallback.index(team_id) + 1}")  # mark fallback with *
            else:
                ranks.append("N/A")

        ranks_str = ' & '.join(str(r) for r in ranks)
        print(f"{team_name} & {ranks_str} \\\\")



if __name__ == '__main__':
    main()
    nfl()
