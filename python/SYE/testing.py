import matplotlib.pyplot as plt

def plot_upsets_per_year(method_upset_dict, years):
    """
    Plots number of upsets per year by method.

    Parameters:
    method_upset_dict (dict): Keys are method names, values are lists of upset counts per year.
    years (list): List of years corresponding to upset values.
    """
    plt.figure(figsize=(10, 6))

    for method, upsets in method_upset_dict.items():
        # Truncate or pad with None if needed to match years
        if len(upsets) < len(years):
            upsets += [None] * (len(years) - len(upsets))
        elif len(upsets) > len(years):
            upsets = upsets[:len(years)]

        plt.plot(years, upsets, marker="o", label=method)

    plt.xlabel("Year")
    plt.ylabel("Number of Upsets")
    plt.title("Upsets Per Year by Ranking Method")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


import matplotlib.pyplot as plt


def scatter_ndcg_vs_playoff_upsets(ndcg_data, playoff_upsets_data):
    """
    Creates a scatter plot of NDCG vs. Playoff Upsets for each method.

    Parameters:
    ndcg_data (dict): Dictionary with method names as keys and average NDCG (float or list of one float) as values.
    playoff_upsets_data (dict): Dictionary with method names as keys and average playoff upsets (float or list of one float) as values.
    """

    def extract_scalar(value):
        return value[0] if isinstance(value, list) else value

    methods = list(ndcg_data.keys())
    ndcg_values = [extract_scalar(ndcg_data[method]) for method in methods]
    playoff_upsets_values = [extract_scalar(playoff_upsets_data[method]) for method in methods]

    plt.figure(figsize=(10, 6))
    plt.scatter(ndcg_values, playoff_upsets_values, color='steelblue')

    # Add labels to each point
    for method, x, y in zip(methods, ndcg_values, playoff_upsets_values):
        plt.text(x + 0.005, y, method, fontsize=9)

    plt.xlabel("Average NDCG")
    plt.ylabel("Average Playoff Upsets")
    plt.title("Scatter Plot of NDCG vs. Playoff Upsets by Method")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


import matplotlib.pyplot as plt

def scatter_ndcg_vs_playoff_upsets_by_year(method_name, ndcg_values, playoff_upsets_values, years):
    """
    Creates a scatter plot for a single method showing NDCG vs. Playoff Upsets across years.

    Parameters:
    method_name (str): The name of the method (e.g., 'Method_1')
    ndcg_dict (dict): Dictionary with method names as keys and lists of NDCG scores over years as values.
    playoff_upsets_dict (dict): Dictionary with method names as keys and lists of playoff upsets over years as values.
    years (list): List of years corresponding to each data point.
    """

    plt.figure(figsize=(10, 6))
    plt.scatter(ndcg_values, playoff_upsets_values, color='darkorange')


    plt.xlabel("NDCG")
    plt.ylabel("Playoff Upsets")
    plt.title(f"NDCG vs. Playoff Upsets by Year for {method_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt
import numpy as np

def plot_grouped_bar_avg_ndcg_ratio(ndcg_dict, ratio_dict):
    """
    Plots a grouped bar chart (side-by-side) of average NDCG and average upset ratio for each method.

    Parameters:
    ndcg_dict (dict): Dictionary where keys are method names and values are lists of NDCG scores.
    ratio_dict (dict): Dictionary where keys are method names and values are lists of upset ratios.
    """
    methods = list(ndcg_dict.keys())
    avg_ndcg = [np.mean(ndcg_dict[method]) for method in methods]
    avg_ratio = [np.mean(ratio_dict[method]) for method in methods]
    labels = ['Linear', 'Nonlinear', 'Least Squares', 'Maximum Likelihood', 'Tournaments', 'Modern']

    x = np.arange(len(methods))
    bar_width = 0.35

    plt.figure(figsize=(12, 6))
    plt.bar(x - bar_width/2, avg_ndcg, width=bar_width, label="Average NDCG", color="skyblue")
    plt.bar(x + bar_width/2, avg_ratio, width=bar_width, label="Average Upset Ratio", color="salmon")

    plt.ylabel("NDCG & Proportion of Games Correct")
    plt.title("NDCG & Proportion of Games Correct")
    plt.xticks(x, labels)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt
import networkx as nx

def draw_digraph_from_matrix(matrix, labels=None):
    """
    Generates a directed graph from an adjacency matrix.

    Parameters:
    - matrix (list of list or np.array): Adjacency matrix representing the digraph.
    - labels (list, optional): Labels for the nodes. Defaults to numeric indices.
    """
    G = nx.DiGraph()

    n = len(matrix)
    if labels is None:
        labels = list(range(n))

    # Add nodes
    for i in range(n):
        G.add_node(labels[i])

    # Add edges
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                G.add_edge(labels[i], labels[j], weight=matrix[i][j])

    pos = nx.spring_layout(G, seed=42)  # consistent layout
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, arrows=True, node_color="lightblue", edge_color="gray", node_size=1500, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
    plt.title("Directed Graph from Adjacency Matrix")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
