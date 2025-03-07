# this is where we will calculate the frobenius norm and fixed point integrals
import math
from math import log

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import lu, solve
from scipy.optimize import fsolve


# functions used for method 1

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

def fixed_point(A, records, eps=1e-100):
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
def linear_strengths(matrix, ranking, records):
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

# functions needed for method 2

# 3.4 in the paper
def f(x):
  result = (0.05*x + x*x) / (2 + 0.05*x + x*x)
  return result

# 3.5
def e(s1, s2):
  result = (5 + s1 + pow(s1, (2/3))) / (5 + s2 + pow(s1, (2/3)))
  return result

def F(matrix, ranking, records):
    '''
    Calculate the strengths based off a ranking array (figure 3.2)
    :param matrix: current matrix we're working with
    :param ranking: ranking vector
    :param records: records of the teams
    :return: the vector of strengths
    '''
    ranks = []
    sum = 0
    for i in range(len(records)):
        for j in range(len(records)):
          if int(matrix[i][j]) == 0 and int(matrix[j][i]) == 0:
              continue
          # inputs the score of the games into the function to calculate e
          e_ij = e(int(matrix[i][j]), int(matrix[j][i]))

          # uses e_ij multiplied by the ranking of the opponent to calculate the strengths
          sum += f(e_ij*ranking[j])

        sum /= (records[i][4]) # divide by number of games
        ranks.append(sum)
        sum = 0
    return ranks

def nonlinear_strengths(matrix, records):
    # repeatedly calls F on ranking vector r until r stabilizes
    all_ranks = []
    r_0 = np.ones(len(records))
    n = 1
    while True:
        r = F(matrix, r_0, records)
        all_ranks.append(r)
        if np.allclose(r_0, r, 1e-10):
             break
        r_0 = r
        n += 1
    # returns ranking vector, number of iterations, and array of all ranking vectors
    return r, n, all_ranks


# functions needed for method 3

def diagonal_entries(i, matrix, n):
    total = 0
    for j in range(n):
        total += (matrix[i][j]**2)

    return total

def make_B_matrix(records, score_matrix):
    # Initialize square matrix for results
    n = len(records)
    matrix = [[0] * n for _ in range(n)]

    # Fill the matrix with match result
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = diagonal_entries(i, score_matrix, n)  # A team doesn't play against itself
            else:
                matrix[i][j] = -1 * (score_matrix[i][j]*score_matrix[j][i])
    return matrix

def inverse_power_method(B, eps=1e-1000):
    # Initial guess for the eigenvector (random)

    n = B.shape[0]
    r = np.ones(n)
    # Normalize the initial guess
    r = r / np.linalg.norm(r)

    # LU decomposition of matrix A
    P, L, U = lu(B)

    iter = 0
    while True:
        # Solve the system using forward and backward substitution
        y = solve(L, r)  # Forward substitution
        r_0 = solve(U, y)  # Backward substitution

        # Normalize the vector to avoid overflow/underflow
        r_0 = r_0 / np.linalg.norm(r_0)

        # Check for convergence
        if np.allclose(r_0, r, eps):
            break

        r = r_0
        iter += 1

    # The result is the eigenvector corresponding to the smallest eigenvalue
    return r_0, iter

def inverse_power_method_two(B, A0, max_iter=1000, tol=1e-8):
    """
    Inverse Power Method to find the eigenvector corresponding to the smallest eigenvalue
    of the matrix B' = B + A0 * I using LU decomposition.

    Args:
    - B (ndarray): The matrix B (n x n).
    - A0 (float): The scalar A0.
    - max_iter (int): Maximum number of iterations.
    - tol (float): Tolerance for convergence.

    Returns:
    - eigvec (ndarray): The eigenvector corresponding to the smallest eigenvalue of B'.
    """

    # Define matrix B' = B + A0 * I
    n = B.shape[0]
    B_prime = B + A0 * np.eye(n)

    # Perform LU decomposition of B'
    P, L, U = lu(B_prime)

    # Initial guess for the eigenvector (random vector)
    eigvec = np.ones(n)

    for _ in range(max_iter):
        # Solve the system B' * eigvec = eigvec using forward and backward substitution
        # First solve L * y = eigvec using forward substitution
        y = np.linalg.solve(L, eigvec)

        # Then solve U * eigvec = y using backward substitution
        eigvec = np.linalg.solve(U, y)

        # Normalize the eigenvector
        eigvec_norm = np.linalg.norm(eigvec)
        eigvec /= eigvec_norm

        # Check for convergence (if the change in the eigenvector is small)
        #if np.linalg.norm(np.dot(B_prime, eigvec) - eigvec) < tol:
            #break
        
        iter = _
    # Return the eigenvector corresponding to the smallest eigenvalue
    return eigvec, iter

# TODO: implement method 3

def alpha(matrix, k):
    """Computes the sum of column k in the matrix."""
    return sum(matrix[j][k] for j in range(len(matrix)))

def func(r_k, matrix, r, k):
    """Defines the function to be solved for r_k."""
    total = alpha(matrix, k) / r_k
    for j in range(len(matrix)):
        total -= ((matrix[j][k] + matrix[k][j]) / (r[j] + r_k))
    return total

def solver(matrix):
    """Solves for r using fsolve for each element iteratively."""
    r = np.ones(len(matrix))  # Initialize r as an array
    for i in range(len(matrix)):
        print(fsolve(func, r[i], args=(matrix, r, i)))
        r[i] = fsolve(func, r[i], args=(matrix, r, i))[0]  # Extract root from fsolve output
    return r

def func2(r, matrix):
    res = np.zeros(len(matrix))
    for k, r_k in enumerate(r):
        res[k] = (func(r_k, matrix, r, k))
    return res


def solver2(matrix):
    r = [0.5] * len(matrix)
    r = np.array(r)
    tmp, info, _, _ = fsolve(func2, r, args=(matrix), full_output=True)
    print(info)
    return tmp

# 5.9
def system(t, r, matrix, _):
    return func2(r, matrix)

def solver3(matrix):
    r = np.ones(len(matrix))
    t_span = (0, 10)
    t_eval = np.linspace(t_span[0], t_span[1], 1000)
    solution = solve_ivp(system, t_span, r, t_eval=t_eval, args=((matrix, 0)))
    ranking = []
    for i in range(len(matrix)):
        ranking.append(solution.y[i][-1])
    return ranking


