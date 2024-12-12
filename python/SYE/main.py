# main file for actually running the program
from build_matrices import build_matrices
from data_manipulation import generate_data
import numpy as np

from matrix_math import fixed_point, output, calc_strengths

# initalize data
games, team_games, records = generate_data('1989.txt')

# build the four matrices we 'need'
results_matrix, weighted_results_matrix, score_matrix, weighted_score_matrix = build_matrices(team_games, records)

matrices = np.array(weighted_score_matrix)
ranking, iter, every_rank = fixed_point(matrices, records)
print(iter)

strengths = calc_strengths(score_matrix, ranking, records)

output(ranking, strengths, records, 40)

