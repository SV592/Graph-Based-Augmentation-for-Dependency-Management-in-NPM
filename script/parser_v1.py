import json
import os


def parse_lockfile_v1(file_path, output_path):
    """
    Parses a lockfile with lockfileVersion 1 and formats it like version 2 files.
    """
    try:
        with open(file_path, "r") as f:
            lock_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {file_path}. Skipping.")
        return

    dependencies = lock_data.get("dependencies", {})
    parsed_dependencies = {}

    def process_dependency(dep_name, dep_info, parent_path=""):
        """
        Processes a single dependency and adds it to the parsed_dependencies map.
        """
        # Extract version
        dep_version = dep_info.get("version", "unknown")

        # Generate unique key
        package_key = f"{dep_name}@{dep_version}"

        # Extract dependencies recursively
        child_dependencies = []
        requires = dep_info.get("requires", {})
        for child_name, child_version in requires.items():
            child_dependencies.append(f"{child_name}@{child_version}")

        # Add to the parsed map
        parsed_dependencies[package_key] = {
            "dependencies": child_dependencies,
            "isDevDependency": dep_info.get("dev", False),
        }

        # Process nested "dependencies" if present (lockfile v1 supports this)
        nested_deps = dep_info.get("dependencies", {})
        for nested_name, nested_info in nested_deps.items():
            process_dependency(nested_name, nested_info, parent_path=f"{dep_name} > ")

    # Process all dependencies
    for dep_name, dep_info in dependencies.items():
        process_dependency(dep_name, dep_info)

    # Write to output
    base_name = os.path.basename(file_path).replace(".json", "_parsed.json")
    output_file = os.path.join(output_path, base_name)
    with open(output_file, "w") as out_f:
        json.dump(parsed_dependencies, out_f, indent=2)
    print(f"Parsed data saved to {output_file}")


def process_directory(input_dir, output_dir):
    """
    Processes all package-lock.json files in the input directory.
    """
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            input_path = os.path.join(input_dir, file_name)
            parse_lockfile_v1(input_path, output_dir)


# Example usage
input_dir = "../empty_files"  # Replace with your input directory
output_dir = "./parsed_files"  # Replace with your desired output directory

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

process_directory(input_dir, output_dir)
