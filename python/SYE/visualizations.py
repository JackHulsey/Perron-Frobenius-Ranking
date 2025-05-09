# visually output our data

import matplotlib.pyplot as plt

def plot_boxplot_upsets(data_dict, title="Upset Distribution", ylabel="Number of Upsets"):
    """
    Plots a box plot for upsets or other yearly metrics across ranking methods.

    Parameters:
    - data_dict: dict[int, list[float or int]]
        Dictionary where keys are method indices (0 to N-1), values are lists of values per year.
    - title: str
        Title of the plot.
    - ylabel: str
        Y-axis label.
    """
    methods = sorted(data_dict.keys())
    data = [data_dict[i] for i in methods]
    print(len(methods))
    labels = ['Linear', 'Nonlinear', 'Least Squares', 'Maximum Likelihood', 'Tournaments', 'Modern', 'NFL Power']

    plt.figure(figsize=(12, 6))
    plt.boxplot(
        data,
        patch_artist=True,
        labels=labels, # Needed to fill boxes with color
        boxprops=dict(facecolor='#009CDE', color='black'),
        capprops=dict(color='black'),
        whiskerprops=dict(color='black'),
        flierprops=dict(markerfacecolor='#009CDE', marker='o', color='black'),
        medianprops=dict(color='black')
    )

    plt.ylabel(ylabel)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_upsets_by_year(upset_data: dict, years):
    """
    Plots a line chart of number of upsets per year for each ranking method.

    Parameters:
    - upset_data (dict): keys are method names, values are lists of upsets per year
    - start_year (int): first year (e.g., 1978)
    - end_year (int): last year (e.g., 2024)
    """
    plt.figure(figsize=(14, 7))

    for method, upsets in upset_data.items():
        if len(upsets) != len(years):
            print(len(upsets), len(years))
            print(f"Warning: Length mismatch for {method}")
            continue
        plt.plot(years, upsets, marker='o', label=method)

    plt.xlabel('Year')
    plt.ylabel('Number of Upsets')
    plt.title('Upsets per Year by Ranking Method')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
