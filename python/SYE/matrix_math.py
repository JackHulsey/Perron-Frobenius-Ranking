# this is where we will calculate the frobenius norm and fixed point integrals
import numpy as np

def frobenius_norm(r):
    '''
    Frobenius norm of a matrix
    :param r: matrix we're passing in
    :return: square root of the sum of all entries squared
    '''
    sum = 0
    for v in r:
        sum += (v*v)
    return np.sqrt(sum)

def fixed_point(A, records, eps=1e-1000):
    '''
    Calculate the fixed point integral of a matrix
    :param A: matrix we're integrating
    :param records: records of the teams to make sure we're going to make the array the right length
    :param eps: the closeness of the values
    :return: the ranking array
    '''
    all_ranks = []
    r_0 = np.ones(len(records))
    A_r = A.dot(r_0)
    denominator = frobenius_norm(A_r)
    A_r /= denominator
    n = 2
    while True:
        A_r = (A.dot(A_r))
        denominator = frobenius_norm(A_r)
        A_r /= denominator
        all_ranks.append(A_r)
        if np.allclose(r_0, A_r, eps):
          break
        r_0 = A_r

        n += 1
        r = A_r
    return r, n, all_ranks

# strength = (1/num_games) * (sum ai*ranking)
def calc_strengths(matrix, ranking, records):
    '''
    Calculate the strengths based off a ranking array (figure 2.1)
    :param matrix: current matrix we're working with
    :param ranking: ranking vector
    :param records: records of the teams
    :return: the vector of strengths
    '''
    strength = []
    sum = 0
    for i in range(len(records)):
        for j in range(len(records)):
          # multiplies 1 or 0 with that teams ranking
          sum += matrix[i][j]*ranking[j]
          # print(matrix[iter][i], rankings[i])
        # print(sum, records[i][4])
        sum /= (records[i][4])
        strength.append(sum)
        sum = 0
    return strength

def output(ranking, strength, records, limit=100, strengths=None):
    s = np.argsort(-ranking)
    iter = 1
    tmp = s[0]
    for num in s:
        if strengths is not None:
            # output with strengths
            print(f"{iter:<3} {records[num][0]:<20} {round(strength[num], 6):<10} {round(strength[tmp] - strength[num], 5)}")
        else:
            # output with records of win-loss-tie
            print(f"{iter:<3} {records[num][0]:<18} {records[num][1]}-{records[num][2]}-{records[num][5]} {round(strength[num], 4)}")
        if iter == limit:
            return
        iter += 1
        tmp = num