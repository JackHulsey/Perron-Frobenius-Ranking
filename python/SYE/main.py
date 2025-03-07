# main file for actually running the program
from os import path

from build_matrices import build_matrices
from data_manipulation import generate_data

from ranking import method_one, method_two, method_three, method_four
from scraping import scrape_cfb_schedule


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

        # build the five matrices we 'need'
        results_matrix, weighted_results_matrix, score_matrix, weighted_score_matrix, raw_score_matrix, A_matrix = build_matrices(team_games, records)

        # print_matrix(raw_score_matrix, records)
        print("\nMethod one: simple linear method using fixed point integrals to determine eigenvectors:")
        method_one(weighted_score_matrix, score_matrix, records, True)
        print("\n\nMethod two: non-linear method using using strength of schedule")
        method_two(results_matrix, raw_score_matrix, score_matrix, records, True)
        print("\n\nMethod three: probabilistic approach of approximating pi_ij as the probability of i beating j")
        method_three(raw_score_matrix, score_matrix, records, True)
        print("\n\nMethod four: the maximum likelihood method (Bradley-Terry model)")
        method_four(A_matrix, records)

if __name__ == '__main__':
    main()
