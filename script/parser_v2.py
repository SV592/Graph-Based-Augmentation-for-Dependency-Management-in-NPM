import json
import os
import re


def extract_name_and_version(package_path, package_info):
    """
    Dynamically extracts the package name and version.
    - Prioritizes `name` and `version` fields from `package_info`.
    - Fallbacks to extracting version from the `package_path` if `version` is unknown.
    """
    # Attempt to get name and version from package_info
    package_name = package_info.get("name", package_path.split("/")[-1])
    package_version = package_info.get("version", "unknown")

    # If version is still unknown, try extracting it from the name
    if package_version == "unknown":
        package_name, extracted_version = extract_version_from_name(package_name)
        if extracted_version != "unknown":
            package_version = extracted_version

    return package_name, package_version


def extract_version_from_name(package_name):
    """
    Extracts the version from a package name if it follows the pattern 'name@version'.
    """
    match = re.match(r"^(.+?)@([\w.-]+)$", package_name)
    if match:
        name, version = match.groups()
        return name, version
    return package_name, "unknown"


def parse_dependencies(packages):
    """
    Parses the 'packages' section of lockfileVersion 2+ and builds a dependency map.
    Excludes the root-level dependencies (e.g., main package dependencies).
    """
    dependency_map = {}

    for package_path, package_info in packages.items():
        # Skip the root package (it has no `name` field but appears as the root key)
        if package_path == "":
            continue

        # Extract name and version dynamically
        package_name, package_version = extract_name_and_version(
            package_path, package_info
        )

        # Determine if this is a dev dependency
        is_dev_dependency = package_info.get("dev", False)

        # Create a unique identifier for the package
        package_identifier = f"{package_name}@{package_version} ({package_path})"

        # Initialize the dependency categories
        dependency_map[package_identifier] = {
            "dependencies": [],
            "peerDependencies": [],
            "optionalDependencies": [],
            "isDevDependency": is_dev_dependency,
        }

        # Process dependencies
        for dep_type in ["dependencies", "peerDependencies", "optionalDependencies"]:
            deps = package_info.get(dep_type, {})
            for dep_name, dep_version in deps.items():
                dep_identifier = f"{dep_name}@{dep_version}"
                dependency_map[package_identifier][dep_type].append(dep_identifier)

    return dependency_map


def process_directory(input_dir, output_dir):
    """
    Loops through all JSON files in the input directory,
    parses them, and saves the output in the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)

            try:
                with open(input_path, "r") as f:
                    lock_data = json.load(f)

                # Parse the packages section
                packages = lock_data.get("packages", {})
                dependency_map = parse_dependencies(packages)

                # Save the parsed dependency map
                with open(output_path, "w") as f:
                    json.dump(dependency_map, f, indent=2)

                print(f"Processed and saved: {file_name}")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")


def main():
    input_dir = "./file"  # Replace with your input directory
    output_dir = "parsed_json_files"  # Replace with your output directory

    process_directory(input_dir, output_dir)
    print("All files have been processed.")


if __name__ == "__main__":
    main()
