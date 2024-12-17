import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def generate_unscrewed_plot(file_path, output_file):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Extract data
    version_mismatch = df["VersionMismatch"]
    most_depended_on = df["MostDependedOnPackage"]

    # Plot setup
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Bar plot for Version Mismatch
    ax1.bar(
        df["Project"],
        version_mismatch,
        color="grey",
        label="Version Mismatch",
        alpha=0.7,
    )
    ax1.set_xlabel("Projects", fontsize=12)
    ax1.set_ylabel("Version Mismatch", fontsize=12, color="grey")
    ax1.tick_params(axis="y", labelcolor="grey")
    ax1.set_xticks(range(len(df["Project"])))
    ax1.set_xticklabels(df["Project"], rotation=90, fontsize=9)

    # Line plot for Most Depended-On Packages
    ax2 = ax1.twinx()
    ax2.plot(
        df["Project"],
        most_depended_on,
        color="blue",
        marker="o",
        label="Most Depended-On Packages",
        alpha=0.7,
    )
    ax2.set_ylabel("Most Depended-On Packages", fontsize=12, color="blue")
    ax2.tick_params(axis="y", labelcolor="blue")

    # Add title and legend
    plt.title("Version Duplication vs. Most Depended-On Packages", fontsize=14)
    fig.tight_layout()
    fig.legend(loc="upper right", bbox_to_anchor=(0.85, 0.85), fontsize=10)

    # Save and show plot
    plt.savefig(output_file, format="png", dpi=300)
    print(f"Unscrewed plot saved to {output_file}")
    plt.show()


# Call the function
generate_unscrewed_plot(
    "npm_dependency_metrics_v2.csv",
    "unscrewed_version_mismatch_vs_dependencies_v1.png",
)
