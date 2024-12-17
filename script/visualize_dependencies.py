import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def generate_dependency_vs_total_packages_chart(
    file_path_v1, file_path_v2, output_file
):
    # Read the CSV files
    df_v1 = pd.read_csv(file_path_v1)
    df_v2 = pd.read_csv(file_path_v2)

    # Calculate averages for version 1
    averages_v1 = {
        "Peer Dependencies": df_v1["TotalPeerDependencies"].mean(),
        "Cyclic Dependencies": df_v1["TotalCyclicDependencies"].mean(),
        "Transitive Dependencies": df_v1["TotalTransitiveDependencies"].mean(),
        "Unused Dependencies": df_v1["UnusedDependencies"].mean(),
        "Optional Dependencies": df_v1["TotalOptionalDependencies"].mean(),
    }
    total_packages_v1 = df_v1["TotalPackages"].mean()

    # Calculate averages for version 2
    averages_v2 = {
        "Peer Dependencies": df_v2["TotalPeerDependencies"].mean(),
        "Cyclic Dependencies": df_v2["TotalCyclicDependencies"].mean(),
        "Transitive Dependencies": df_v2["TotalTransitiveDependencies"].mean(),
        "Unused Dependencies": df_v2["UnusedDependencies"].mean(),
        "Optional Dependencies": df_v2["TotalOptionalDependencies"].mean(),
    }
    total_packages_v2 = df_v2["TotalPackages"].mean()

    # Normalize values as percentages relative to total packages for each version
    normalized_averages_v1 = {
        key: (value / total_packages_v1) * 100 for key, value in averages_v1.items()
    }
    normalized_averages_v2 = {
        key: (value / total_packages_v2) * 100 for key, value in averages_v2.items()
    }

    # Apply logarithmic transformation
    skewed_values_v1 = {
        key: np.log10(value + 1) for key, value in normalized_averages_v1.items()
    }
    skewed_values_v2 = {
        key: np.log10(value + 1) for key, value in normalized_averages_v2.items()
    }

    # Data for radar chart
    labels = list(skewed_values_v1.keys())

    # Ensure order of labels is consistent between v1 and v2
    # (Assumes both have the same keys in the same order)
    values_v1 = [skewed_values_v1[label] for label in labels]
    values_v2 = [skewed_values_v2[label] for label in labels]

    # Close the loop for radar chart
    values_v1 += values_v1[:1]
    values_v2 += values_v2[:1]

    # Radar chart setup
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # Determine the max radius for the plot based on both datasets
    max_val = max(max(values_v1), max(values_v2))

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Plot version 1 data
    ax.fill(angles, values_v1, color="blue", alpha=0.25)
    ax.plot(angles, values_v1, color="blue", linewidth=2, label="Version 1")

    # Add actual averages as annotations for version 1
    for angle, label, val, raw_val in zip(
        angles, labels, values_v1, averages_v1.values()
    ):
        ax.text(
            angle,
            val + 0.1,
            f"{int(raw_val)}",
            color="blue",
            fontsize=9,
            ha="center",
        )

    # Plot version 2 data
    ax.fill(angles, values_v2, color="red", alpha=0.25)
    ax.plot(angles, values_v2, color="red", linewidth=2, label="Version 2")

    # Add actual averages as annotations for version 2
    # To avoid clutter, shift these slightly further out or in a different direction.
    for angle, label, val, raw_val in zip(
        angles, labels, values_v2, averages_v2.values()
    ):
        ax.text(
            angle,
            val + 0.2,  # Slightly higher than v1 annotations
            f"{int(raw_val)}",
            color="red",
            fontsize=9,
            ha="center",
        )

    # Add average total packages for both versions as a label outside the radar chart
    annotation_text = (
        f"Avg Total Packages (V1): {int(total_packages_v1)}\n"
        f"Avg Total Packages (V2): {int(total_packages_v2)}"
    )
    ax.text(
        -np.pi / 2,
        max_val + 0.5,
        annotation_text,
        color="black",
        fontsize=11,
        ha="center",
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"),
    )

    # Format the chart
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)

    # Set grid and limits
    ax.set_ylim(0, max_val + 0.5)
    ax.yaxis.grid(True, color="gray", linestyle="dotted", linewidth=0.5)
    ax.set_yticklabels([])  # Remove decimal labels on the y-axis

    # Add title and legend
    ax.set_title("Dependency Relationships vs. Total Packages", fontsize=14, pad=30)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.2), fontsize=10)

    plt.tight_layout()
    plt.savefig(output_file, format="png", dpi=300)
    print(f"Chart saved to {output_file}")
    plt.show()


# Example of calling the modified function
generate_dependency_vs_total_packages_chart(
    "npm_dependency_metrics_v1.csv",
    "npm_dependency_metrics_v2.csv",
    "dependency_vs_total_packages_compare.png",
)
