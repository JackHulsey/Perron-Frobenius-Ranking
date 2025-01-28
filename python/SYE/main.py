# main file for actually running the program
from build_matrices import build_matrices
from data_manipulation import generate_data
import numpy as np

from matrix_math import fixed_point, output, linear_strengths, nonlinear_strengths
from output_matrices import print_matrix
from ranking import method_one, method_two, method_three

def main():
    # initalize data
    games, team_games, records = generate_data('data/1989.txt', verbose = True)

    # build the five matrices we 'need'
    results_matrix, weighted_results_matrix, score_matrix, weighted_score_matrix, raw_score_matrix = build_matrices(team_games, records)

    # print_matrix(raw_score_matrix, records)

    # method_one(weighted_score_matrix, score_matrix, records)
    print("\n")
    # method_two(raw_score_matrix, records, True)

    method_three(raw_score_matrix, records, True)

if __name__ == '__main__':
    main()
