# main file for actually running the program
import os

from build_matrices import build_matrices
from data_manipulation import generate_data
import numpy as np

from output_matrices import print_matrix
from ranking import method_one, method_two, method_three, method_four
from scraping import scrape_cfb_schedule


def main():
    # initalize data
    year = int(input("Enter year: "))

    # Check if the file already exists
    if not os.path.exists(f"data/{year}.txt"):
        scrape_cfb_schedule(year)

    # scrape_cfb_schedule(year)
    games, team_games, records = generate_data(f'data/{year}.txt')

    # build the five matrices we 'need'
    results_matrix, weighted_results_matrix, score_matrix, weighted_score_matrix, raw_score_matrix, A_matrix = build_matrices(team_games, records)

    print_matrix(raw_score_matrix, records)
    print("")
    method_one(weighted_score_matrix, score_matrix, records, True)
    print("\n")
    method_two(results_matrix, raw_score_matrix, score_matrix, records, True)
    print("\n")
    method_three(raw_score_matrix, score_matrix, records, True)

    method_four(A_matrix, records)

if __name__ == '__main__':
    main()
