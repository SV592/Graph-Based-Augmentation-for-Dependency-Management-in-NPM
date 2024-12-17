import pandas as pd
import matplotlib.pyplot as plt


def generate_graph_density_comparison(file_path_v1, file_path_v2, output_file):
    # Read the CSV files
    df_v1 = pd.read_csv(file_path_v1)
    df_v2 = pd.read_csv(file_path_v2)

    # Ensure both DataFrames have the same projects in the same order
    projects_v1 = df_v1["Project"]
    graph_density_v1 = df_v1["GraphDensity"]

    projects_v2 = df_v2["Project"]
    graph_density_v2 = df_v2["GraphDensity"]

    # Plot the line chart
    plt.figure(figsize=(14, 7))  # Adjust the size as needed

    # Plot Version 1 line
    plt.plot(
        projects_v1,
        graph_density_v1,
        marker="o",
        color="blue",
        label="Graph Density - Version 1",
        linewidth=1,
    )

    # Plot Version 2 line
    plt.plot(
        projects_v2,
        graph_density_v2,
        marker="s",
        color="red",
        label="Graph Density - Version 2",
        linewidth=1,
    )

    # Add labels, title, and legend
    plt.xlabel("Projects", fontsize=12)
    plt.ylabel("Graph Density", fontsize=12)
    plt.title("Graph Density Comparison Across Projects", fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(fontsize=10)
    plt.grid(axis="y", linestyle="--", linewidth=0.5)
    plt.legend(fontsize=10, loc="upper right")

    # Tight layout and save the chart
    plt.tight_layout()
    plt.savefig(output_file, format="png", dpi=300)
    print(f"Chart saved to {output_file}")
    plt.show()


# Example usage:
generate_graph_density_comparison(
    "npm_dependency_metrics_v1.csv",
    "npm_dependency_metrics_v2.csv",
    "graph_density_comparison_line_chart.png",
)
