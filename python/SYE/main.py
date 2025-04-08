# main file for actually running the program
import csv

import numpy as np
from os import path

from Evaluations import compare_rankings, upsets, playoffs
from data_manipulation import generate_data, load_rankings_from_csv, get_ap_rankings
from ranking import generate_rankings, comparison
from scraping import scrape_cfb_schedule
from visualizations import plot_boxplot_upsets


def main():
    # initalize NCAA
    league = 'NCAA'
    years = [2000 + i for i in range(25)]
    num_rankings = 7
    ndcg_dict = {i:[] for i in range(num_rankings)}
    num_upsets = {i:[] for i in range(num_rankings+1)}
    ratio_upsets = {i:[] for i in range(num_rankings+1)}
    top_25_dict = {i:[] for i in range(num_rankings+1)}
    top_25_ratio = {i:[] for i in range(num_rankings+1)}
    correct = {i:0 for i in range(num_rankings+1)}
    # generate_rankings(years, 'NCAA')

    for year in years:
        if year == 2020:
            continue
        # print(f"Evaluations from {year}:")
        # Check if the file already exists
        if not path.exists(f"NCAA/{year}.txt"):
            success = scrape_cfb_schedule(year)
        else:
            success = True

        if success:
            games, team_games, records, championship, postseason = generate_data(f'{league}/{year}.txt')
            print(championship)
            ap_rankings, ap_indices = get_ap_rankings(year, records)
            rankings = load_rankings_from_csv(f'rankings/{league}/rankings_{year}.csv', len(records))
            shorter_rankings = [r[:25] for r in rankings]
            ideal, ndcg = compare_rankings(ap_indices, shorter_rankings)
            upset = upsets(shorter_rankings, records, team_games, rankings, ap_indices)
            # comparison(shorter_rankings[0], shorter_rankings[1], shorter_rankings[2], shorter_rankings[3], shorter_rankings[4], shorter_rankings[5], ap_rankings, records)
            for i in range(len(records)):
                if records[i][0] == championship[0]:
                    champion = i
            print(champion, championship[0])
            for i in range(len(rankings)):
                ndcg_dict[i].append(ndcg[i])
                num_upsets[i].append(upset[i][0])
                ratio_upsets[i].append(upset[i][1])
                top_25_dict[i].append(upset[i][2])
                top_25_ratio[i].append(upset[i][3])

                if rankings[i][0] == champion:
                    correct[i] += 1
                print(f"{year} | Method_{i+1}: | ndcg: {round(float(ndcg[i]), 5):<7} |  number of upsets: {upset[i][0]:<4} | ratio: {round(upset[i][1], 4):<9} | Upsets Within top 25: {upset[i][2]} | Upsets Within top 25 ratio: {round(upset[i][3], 2)} | national champ: {rankings[i][0] == champion, records[rankings[i][0]][0]}")
            num_upsets[num_rankings].append(upset[-1][0])
            ratio_upsets[num_rankings].append(upset[-1][1])
            top_25_dict[num_rankings].append(upset[-1][2])
            top_25_ratio[num_rankings].append(upset[-1][3])
            print(f"{year} | AP_Polls: | ndcg: {1:<7} |  number of upsets: {upset[-1][0]:<4} | ratio: {round(upset[-1][1], 4):<9} | Upsets Within top 25: {upset[-1][2]:<4} | Upsets Within top 25 ratio: {upset[-1][3]:<4}\n{year+1}\n")

    print(f"{years[0]}-{years[-1]}")
    print(f"AP_Polls | avg_ndcg: {1.0:<5} | avg_upsets: {round(np.average(num_upsets[num_rankings]), 2):<6} | avg_ratio: {round(np.average(ratio_upsets[num_rankings]), 4):<6} | Upsets Within top 25: {round(np.average(top_25_dict[num_rankings]), 3):<4} | Upsets Within top 25 ratio: {round(np.average(top_25_ratio[num_rankings]), 4)}")
    for i in range(len(ndcg_dict)):
        print(f"Method_{i+1} | avg_ndcg: {round(np.average(ndcg_dict[i]), 2):<5} | avg_upsets: {round(np.average(num_upsets[i]), 3):<6} | avg_ratio: {round(np.average(ratio_upsets[i]), 4):<4} | Upsets Within top 25: {round(np.average(top_25_dict[i]), 3)} | Upsets Within top 25 ratio: {round(np.average(top_25_ratio[i]), 4)} | {correct[i]}")
    plot_boxplot_upsets(num_upsets)
    plot_boxplot_upsets(top_25_dict, 'Top 25 Upsets')

def nfl():
    years = [1999 + i for i in range(1, 26)]
    num_rankings = 7
    upsets_dict = {i:[] for i in range(num_rankings)}
    generate_rankings(years, 'NFL')
    for year in years:
        if year == 2020:
            continue

        games, team_games, records, postseason = generate_data(f'NFL/{year}.txt')
        rankings = load_rankings_from_csv(f'rankings/NFL/rankings_{year}.csv', len(records))
        playoff_upsets = playoffs(rankings, records, postseason)
        for i in range(len(rankings)):
            upsets_dict[i].append(playoff_upsets[i])
            print(f"Method_{i+1} | Playoff upsets: {playoff_upsets[i]:<2} | ratio: {round(playoff_upsets[i] / len(postseason), 4):<9}")
    print(f"{years[0]}-{years[-1]}")
    for i in range(len(rankings)):
        print(f"Method_{i+1} | Playoff upsets: {round(np.average(upsets_dict[i]), 2)} | ratio: {round(np.average(playoff_upsets[i]) / len(postseason), 4):<9} ")


if __name__ == '__main__':
    main()
    # nfl()
