import json
from py2neo import Graph, Node, Relationship
from tqdm import tqdm  # Import tqdm for the progress bar


def parse_dependency_entry(dep_entry):
    """
    Parses a dependency entry string to extract the dependency's name, version, and path.
    Expected format: "package_name@version (package_path)".
    If no explicit version or path is found, defaults to 'unknown' for missing values.
    """
    dep_path = ""
    if " (" in dep_entry:
        name_version_part, dep_path = dep_entry.split(" (", 1)
        dep_path = dep_path.rstrip(")")
    else:
        name_version_part = dep_entry

    # Extract the package name and version
    if "@" in name_version_part:
        dep_name, dep_version = name_version_part.rsplit("@", 1)
    else:
        dep_name, dep_version = name_version_part, "unknown"

    return dep_name.strip(), dep_version.strip(), dep_path.strip()


def import_dependencies_to_neo4j(dependency_map, graph):
    """
    Imports dependency relationships into Neo4j.
    Each key in dependency_map represents a package and its dependencies.
    """
    # Neo4j connection details
    neo4j_uri = ""  # Adjust if needed
    username = ""  # Default username
    password = ""  # Replace with your actual password

    # Connect to Neo4j
    graph_db = Graph(neo4j_uri, auth=(username, password))

    # Begin a transaction for performance
    tx = graph_db.begin()

    node_cache = {}

    print("Starting import of dependencies into Neo4j...")

    # Use tqdm for a progress bar
    with tqdm(
        total=len(dependency_map), desc="Processing Packages", unit="pkg"
    ) as pbar:
        for package_entry, dependencies_info in dependency_map.items():
            # Parse the package name, version, and path
            package_name, package_version, package_path = parse_dependency_entry(
                package_entry
            )
            package_key = f"{package_name}|{package_version}"

            # Ensure path is set for the package
            package_path = package_path or f"node_modules/{package_name}"

            # Create or retrieve the node for the package
            if package_key not in node_cache:
                package_node = Node(
                    "Package",
                    name=package_name,
                    version=package_version,
                    path=package_path,
                )
                tx.merge(package_node, "Package", ("name", "version"))
                node_cache[package_key] = package_node
            else:
                package_node = node_cache[package_key]

            # Iterate through dependency types (dependencies, peerDependencies, etc.)
            for dep_type, dep_list in dependencies_info.items():
                if dep_type == "isDevDependency":
                    continue  # Skip this key; it doesn't represent a relationship

                for dep_entry in dep_list:
                    # Parse the dependency's name, version, and path
                    dep_name, dep_version, dep_path = parse_dependency_entry(dep_entry)
                    dep_key = f"{dep_name}|{dep_version}"

                    # Ensure path is set for the dependency
                    dep_path = dep_path or f"{package_path}/node_modules/{dep_name}"

                    # Create or retrieve the node for the dependency
                    if dep_key not in node_cache:
                        dep_node = Node(
                            "Package",
                            name=dep_name,
                            version=dep_version,
                            path=dep_path,
                        )
                        tx.merge(dep_node, "Package", ("name", "version"))
                        node_cache[dep_key] = dep_node
                    else:
                        dep_node = node_cache[dep_key]

                    # Create the relationship
                    rel_type = (
                        dep_type.upper()
                    )  # Use dependency type as the relationship
                    rel = Relationship(package_node, rel_type, dep_node)
                    tx.merge(rel)

            # Update the progress bar
            pbar.update(1)

    # Commit the transaction
    tx.commit()
    print("Dependency graph imported into Neo4j successfully!")


def main():
    # Load the dependency map JSON
    input_file = "../parsed_json_files_v2/commanderjs.json"
    print(f"Loading dependency map from {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        dependency_map = json.load(f)

    print("Dependency map loaded. Starting import...")
    # Connect to Neo4j
    neo4j_uri = ""  # Adjust if needed
    username = ""  # Default username
    password = ""  # Replace with your actual password
    graph = Graph(neo4j_uri, auth=(username, password))

    # Import dependencies into Neo4j
    import_dependencies_to_neo4j(dependency_map, graph)


if __name__ == "__main__":
    main()
