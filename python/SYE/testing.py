import csv


def merge_and_count(arr, temp_arr, left, right):
    inv_count = 0
    if left < right:
        mid = (left + right) // 2
        inv_count += merge_and_count(arr, temp_arr, left, mid)
        inv_count += merge_and_count(arr, temp_arr, mid + 1, right)
        inv_count += merge(arr, temp_arr, left, mid, right)
    return inv_count


def merge(arr, temp_arr, left, mid, right):
    i = left  # Starting index for left subarray
    j = mid + 1  # Starting index for right subarray
    k = left  # Starting index to be sorted
    inv_count = 0

    # Conditions are checked to ensure that i doesn't exceed mid and j doesn't exceed right
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp_arr[k] = arr[i]
            i += 1
        else:
            temp_arr[k] = arr[j]
            inv_count += (mid - i + 1)
            j += 1
        k += 1

    # Copy the remaining elements of left subarray, if any
    while i <= mid:
        temp_arr[k] = arr[i]
        i += 1
        k += 1

    # Copy the remaining elements of right subarray, if any
    while j <= right:
        temp_arr[k] = arr[j]
        j += 1
        k += 1

    # Copy the sorted subarray into the original array
    for i in range(left, right + 1):
        arr[i] = temp_arr[i]

    return inv_count


def count_inversions(arr, sorted_list):
    # Filter out elements not in the sorted_list
    filtered_arr = [x for x in arr if x in sorted_list]

    # Create a temporary array to assist merge sort
    temp_arr = [0] * len(filtered_arr)

    return merge_and_count(filtered_arr, temp_arr, 0, len(filtered_arr) - 1)


def load_rankings_from_csv(file_name, length):
    rankings = {f"Method_{i+1}": [None] * length for i in range(6)}  # Assuming max rank 130
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            year, method, rank, team = row
            rank = int(rank)
            team = int(team)
            rankings[method][rank - 1] = team  # Index by rank (0-based)
    return [rankings[f"Method_{i+1}"] for i in range(6)]

def ranking_analysis(year, records):
    rankings = load_rankings_from_csv(f'rankings/rankings-{year}.csv', len(records))




# print(load_rankings_from_csv('rankings/rankings_2024.csv', 129)[5])