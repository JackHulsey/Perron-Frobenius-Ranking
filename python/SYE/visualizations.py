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
    labels = [f"Method_{i+1}" for i in methods]

    plt.figure(figsize=(12, 6))
    plt.boxplot(data, labels=labels, patch_artist=True)

    plt.title(title)
    plt.xlabel("Ranking Method")
    plt.ylabel(ylabel)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
