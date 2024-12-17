import time
import os
import csv
from py2neo import Graph
from tqdm import tqdm


def run_query_with_timer(graph, query):
    """
    Run a query and measure its execution time.
    """
    start_time = time.time()
    result = graph.run(query).data()
    runtime = time.time() - start_time
    return result, runtime


def main(project_name):
    """
    Main function to run queries on the Neo4j graph and save metrics to a CSV file.
    """
    # Neo4j connection details
    neo4j_uri = ""  # Adjust if needed
    username = ""  # Default username
    password = ""  # Replace with your actual password
    graph = Graph(neo4j_uri, auth=(username, password))

    # Queries
    queries = {
        "TotalPackages": """
            MATCH (p:Package)
            RETURN COUNT(p) AS TotalPackages;
        """,
        "TotalTransitiveDependencies": """
           MATCH (p:Package)-[:DEPENDENCIES|PEERDEPENDENCIES|OPTIONALDEPENDENCIES*2..]->(d:Package)
           RETURN COUNT(DISTINCT d) AS TotalTransitiveDependencies;
        """,
        "TotalCyclicDependencies": """
            MATCH path = (p:Package)-[:DEPENDENCIES|PEERDEPENDENCIES|OPTIONALDEPENDENCIES*]->(p)
            RETURN COUNT(path) AS TotalCyclicDependencies;
        """,
        "TotalOptionalDependencies": """
            MATCH ()-[r:OPTIONALDEPENDENCIES]->()
            RETURN COUNT(r) AS TotalOptionalDependencies;
        """,
        "TotalPeerDependencies": """
           MATCH ()-[r:PEERDEPENDENCIES]->()
           RETURN COUNT(r) AS TotalPeerDependencies;
        """,
        "GraphDensity": """
            MATCH (p:Package)
            WITH COUNT(p) AS nodes
            MATCH ()-[r:DEPENDENCIES|PEERDEPENDENCIES|OPTIONALDEPENDENCIES]->()
            WITH nodes, COUNT(r) AS edges
            RETURN edges, nodes, (2.0 * edges) / (nodes * (nodes - 1)) AS Density;
        """,
        "AveragePathLength": """
            MATCH path = (p:Package)-[:DEPENDENCIES|PEERDEPENDENCIES|OPTIONALDEPENDENCIES*]->(d:Package)
            RETURN AVG(LENGTH(path)) AS AvgPathLength;
        """,
        "UnusedDependencies": """
            MATCH (p:Package)
            WHERE NOT (p)-[:DEPENDENCIES]->() AND NOT ()-[:DEPENDENCIES]->(p)
            RETURN COUNT(p) AS TotalUnusedDependencies;
        """,
        "MostDependedOnPackage": """
           MATCH (p:Package)<-[r:DEPENDENCIES|PEERDEPENDENCIES|OPTIONALDEPENDENCIES]-()
           WITH p, COUNT(r) AS ProjectsDependingOn
           ORDER BY ProjectsDependingOn DESC
           LIMIT 1
           RETURN ProjectsDependingOn;
        """,
        "VersionMismatch": """
           MATCH (p1:Package)-[:DEPENDENCIES|PEERDEPENDENCIES|OPTIONALDEPENDENCIES]->(d1:Package),
                 (p2:Package)-[:DEPENDENCIES|PEERDEPENDENCIES|OPTIONALDEPENDENCIES]->(d2:Package)
           WHERE d1.path = d2.path AND d1.version <> d2.version
           WITH d1.path AS Path, COLLECT(DISTINCT d1.version) AS Versions
           WITH Path, Versions, SIZE(Versions) AS VersionCount
           WHERE VersionCount > 1
           RETURN COUNT(Path) AS TotalVersionMismatches;
        """,
    }

    # Run queries and collect results
    metrics = {"Project": project_name}
    query_list = list(queries.items())

    with tqdm(total=len(query_list), desc="Running All Queries", unit="query") as pbar:
        for metric, query in query_list:
            result, runtime = run_query_with_timer(graph, query)
            value_key = list(result[0].keys())[0] if result else None
            metrics[metric] = result[0].get(value_key, 0) if result else 0
            pbar.update(1)

    # Save to CSV
    output_file = "npm_dependency_metrics.csv"
    file_exists = os.path.isfile(output_file)

    with open(output_file, mode="a", newline="") as file:
        fieldnames = ["Project"] + list(queries.keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(metrics)

    print(f"Metrics for {project_name} saved to {output_file}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python query_graph.py <project_name>")
        exit(1)

    project_name = sys.argv[1]
    main(project_name)
