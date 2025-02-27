import numpy as np

from matrix_math import fixed_point, linear_strengths, nonlinear_strengths, \
    inverse_power_method, make_B_matrix, inverse_power_method_two, solver

def output(ranking, records, limit=100, strength=None, three=False):
    if strength:
        strength = np.array(strength)
        s = np.argsort(-strength)
    else:
        ranking = np.array(ranking)
        if three:
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
            if three:
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

def method_four(A_matrix, records):
    ranking = solver(A_matrix)
    output(ranking, records)






