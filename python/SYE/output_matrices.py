# a file to contain functions to print out matrices cleanly
# may add more functions to graphically show the change in ranking as we rank them.

def standardize_lengths(records):
    # shortens team names to standardize the matrix
    std_teams = []
    for i in range(len(records)):
        std_teams.append(records[i][0])
        std_teams[i] = std_teams[i][:10]
    return std_teams

def print_matrix(matrix, records):
    # Display the results matrix
    print(f"{' ':<12}", end="")
    std_teams = standardize_lengths(records)
    for team in std_teams:
        print(f"{team:<12}", end="")
    print()
    for i, row in enumerate(matrix):
        print(f"{std_teams[i]:<12}", end="")
        for result in row:
            print(f"{str(result):<12}", end="")
        print()