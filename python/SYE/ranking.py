import numpy as np

from matrix_math import fixed_point, linear_strengths, nonlinear_strengths, \
    inverse_power_method, make_B_matrix, inverse_power_method_two, solver, solver2, solver3, tournament, modern


def output(ranking, records, limit=100, strength=None, reverse=False):
    if strength:
        strength = np.array(strength)
        s = np.argsort(-strength)
    else:
        ranking = np.array(ranking)
        if reverse:
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
            if reverse:
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
        print("\nMethod one: simple linear method using fixed point integrals to determine eigenvectors:")
        print(f"Iterations of fixed point integral: {iter}")
        strengths = linear_strengths(score_matrix, ranking, records)
        output(ranking, records, limit=len(records), strength=strengths)
    return np.argsort(np.array(-ranking))

def method_two(results_matrix, raw_score_matrix, score_matrix, records, verbose = False):
    ranking, iter, every_rank = nonlinear_strengths(raw_score_matrix, records)
    ranking = np.array(ranking)
    if verbose:
        print("\n\nMethod two: non-linear method using using strength of schedule")
        print(f"iterations of function F: {iter}")
        output(ranking, records, 40)
    return np.argsort(-np.array(ranking))

def method_three(raw_score_matrix, score_matrix, records, verbose = False):
    B = make_B_matrix(records, raw_score_matrix)
    B = np.array(B)

    ranking, iter = inverse_power_method(B)
    if verbose:
        print("\n\nMethod three: probabilistic approach of approximating pi_ij as the probability of i beating j")
        print(f"iterations of F: {iter}")
        #strengths = linear_strengths(score_matrix, ranking, records)
        output(ranking, records, 40, reverse=True)
    return np.argsort(np.array(ranking))

def method_four(A_matrix, records, verbose=False):
    ranking = solver3(A_matrix)
    if verbose:
        print("\n\nMethod four: the maximum likelihood method (Bradley-Terry model)")
        output(ranking, records, reverse=True, limit=40)
    return np.argsort(np.array(ranking))

def method_five(raw_matrix, records, verbose=False):
    ranking = tournament(raw_matrix)
    if verbose:
        print("\n\nMethod five: a graph theory perspective using tournaments")
        output(ranking, records, reverse=True, limit=40)
    return np.argsort(np.array(ranking))

def method_six(matrix, records, verbose=False):
    ranking = modern(matrix)
    if verbose:
        print("\n\nMethod six: taking a modern approach with scipy.linalg.eig")
        output(ranking, records, limit=len(records), reverse=True)
    # TODO: fix this so that the ranking outputs reversed when it needs to be
    ranking = np.argsort(np.array(ranking))
    if records[ranking[0]][1] < records[ranking[-1]][1]:
        print(records[ranking[0]])
        return ranking[::-1]
    return ranking

def convert(r, records):
    team_rankings = []
    for num in r:
        team_rankings.append(records[num][0])
    return team_rankings

def comparison(r_1, r_2, r_3, r_4, r_5, r_6, r_ap, records):
    r_1 = convert(r_1, records)
    r_2 = convert(r_2, records)
    r_3 = convert(r_3, records)
    r_4 = convert(r_4, records)
    r_5 = convert(r_5, records)
    r_6 = convert(r_6, records)
    for i in range(len(r_ap)):
        print(f"{i+1:<4}: ap: {r_ap[i]:<15} 1: {r_1[i]:<15} 2: {r_2[i]:<15} 3: {r_3[i]:<15} 4: {r_4[i]:<15} 5: {r_5[i]:<15} 6: {r_6[i]:<15}")





