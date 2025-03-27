# main file for actually running the program
from os import path

from Evaluations import kendall_tau, compare_rankings
from matrices.build_matrices import build_matrices
from data_manipulation import generate_data

from ranking import method_one, method_two, method_three, method_four, method_five, method_six, comparison
from scraping import scrape_cfb_schedule, get_college_football_rankings


def main():
    # initalize data
    year = int(input("Enter year: "))

    # Check if the file already exists
    if not path.exists(f"data/{year}.txt"):
        success = scrape_cfb_schedule(year)
    else:
        success = True

    if success:
        games, team_games, records = generate_data(f'data/{year}.txt')
        ap_rankings, ap_indices = get_college_football_rankings(year, records)
        # build the five matrices we 'need'
        results_matrix, weighted_results_matrix, score_matrix, weighted_score_matrix, raw_score_matrix, A_matrix = build_matrices(team_games, records)

        # print_matrix(raw_score_matrix, records)
        # print("\nMethod one: simple linear method using fixed point integrals to determine eigenvectors:")
        ranking_one = method_one(weighted_score_matrix, score_matrix, records, verbose=True)
        # print("\n\nMethod two: non-linear method using using strength of schedule")
        ranking_two = method_two(results_matrix, raw_score_matrix, score_matrix, records)
        # print("\n\nMethod three: probabilistic approach of approximating pi_ij as the probability of i beating j")
        ranking_three = method_three(raw_score_matrix, score_matrix, records)
        # print("\n\nMethod four: the maximum likelihood method (Bradley-Terry model)")
        ranking_four = method_four(A_matrix, records)
        # print("\n\nMethod five: a graph theory perspective using tournaments")
        ranking_five = method_five(raw_score_matrix, records)
        # print("\n\nMethod six: taking a modern approach with scipy.linalg.eig")
        ranking_six = method_six(weighted_score_matrix, records)

        comparison(ranking_one, ranking_two, ranking_three, ranking_four, ranking_five, ranking_six, ap_rankings, records)

        print(kendall_tau(ap_rankings, ranking_one[:25]))
        print(compare_rankings(ap_rankings, ranking_one[:25]))
if __name__ == '__main__':
    main()
