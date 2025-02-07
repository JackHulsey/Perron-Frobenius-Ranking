# main file for actually running the program
from build_matrices import build_matrices
from data_manipulation import generate_data
import numpy as np

from output_matrices import print_matrix
from ranking import method_one, method_two, method_three

def main():
    # initalize data
    games, team_games, records = generate_data('data/1989.txt')

    # build the five matrices we 'need'
    results_matrix, weighted_results_matrix, score_matrix, weighted_score_matrix, raw_score_matrix = build_matrices(team_games, records)

    # print_matrix(raw_score_matrix, records)
    print("")
    method_one(weighted_score_matrix, score_matrix, records, True)
    print("\n")
    method_two(results_matrix, raw_score_matrix, score_matrix, records, True)
    print("\n")
    method_three(raw_score_matrix, score_matrix, records, True)

if __name__ == '__main__':
    main()
