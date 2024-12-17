import os
import json
from py2neo import Graph
from knowledge_graph import import_dependencies_to_neo4j


def clear_neo4j_graph(graph):
    """
    Clears all data from the Neo4j database.
    """
    graph.run("MATCH (n) DETACH DELETE n")
    print("Existing graph data cleared.")


def construct_graph_from_json(json_file, graph):
    """
    Constructs a Neo4j graph from a single JSON file.
    """
    print(f"Constructing graph for: {json_file}")
    with open(json_file, "r", encoding="utf-8") as f:
        dependency_map = json.load(f)
        import_dependencies_to_neo4j(dependency_map, graph)
    print(f"Graph constructed for: {json_file}")


def run_query_script(query_script_path, project_name):
    """
    Runs the query script to execute queries and save metrics.
    """
    print(f"Running query script for {project_name}...")
    os.system(f"python {query_script_path} {project_name}")  # Pass project_name
    print(f"Query script completed for {project_name}.")


def main():
    # Neo4j connection details
    neo4j_uri = ""  # Adjust if needed
    username = ""  # Default username
    password = ""  # Replace with your actual password
    graph = Graph(neo4j_uri, auth=(username, password))

    # Paths and directories
    json_dir = "../parsed_json_files_v1"  # Replace with your JSON directory path
    query_script_path = "query_graph.py"  # Replace with your query script path

    # Process each JSON file
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            json_file = os.path.join(json_dir, filename)

            # Clear existing graph
            clear_neo4j_graph(graph)

            # Construct graph
            construct_graph_from_json(json_file, graph)

            # Extract project name from filename
            project_name = os.path.splitext(os.path.basename(json_file))[0]

            # Run query script
            run_query_script(query_script_path, project_name)


if __name__ == "__main__":
    main()
