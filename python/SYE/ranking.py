import numpy as np

from matrix_math import fixed_point, linear_strengths, output, nonlinear_strengths, \
    inverse_power_method, make_B_matrix, inverse_power_method_two

def method_one(weighted_score_matrix, score_matrix, records, verbose = False):
    matrices = np.array(weighted_score_matrix)
    ranking, iter, every_rank = fixed_point(matrices, records)
    if verbose:
        print(f"Iterations of fixed point integral: {iter}")
    strengths = linear_strengths(score_matrix, ranking, records)
    output(ranking, records, 40, strengths)

def method_two(results_matrix, raw_score_matrix, score_matrix, records, verbose = False):
    ranking, iter, every_rank = nonlinear_strengths(raw_score_matrix, records)
    ranking = np.array(ranking)
    if verbose:
        print(f"iterations of function F: {iter}")
    strengths = linear_strengths(results_matrix, ranking, records)
    output(ranking, records, 40)

def method_three(raw_score_matrix, score_matrix, records, verbose = False):
    B = make_B_matrix(records, raw_score_matrix)
    B = np.array(B)

    ranking, iter = inverse_power_method(B)
    if verbose:
        print(f"iterations of F: {iter}")
    #strengths = linear_strengths(score_matrix, ranking, records)
    output(ranking, records, 40, three=True)


