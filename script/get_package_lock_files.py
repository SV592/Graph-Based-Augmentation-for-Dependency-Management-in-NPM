import csv
import random
import requests
import os

# Configurations
csv_file = "700_commits"  # Replace with your CSV file name
output_dir = "json_files"
token = ""  # Replace with your GitHub token
headers = {"Authorization": f"token {token}"}
target_count = 94

# Create output directory
os.makedirs(output_dir, exist_ok=True)


def fetch_package_lock(repo_url, repo_name):
    api_url = (
        repo_url.replace("https://github.com/", "https://api.github.com/repos/")
        + "/contents/package-lock.json"
    )
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        if content.get("encoding") == "base64":
            file_path = os.path.join(output_dir, f"{repo_name}.json")
            with open(file_path, "wb") as file:
                file.write(
                    requests.get(content["download_url"], headers=headers).content
                )
            return True
    return False


# Load projects
with open(csv_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    projects = list(reader)

# Randomly select projects until we have 94 valid files
valid_count = 0
selected_projects = set()

while valid_count < target_count:
    project = random.choice(projects)
    repo_name = project["Name"]
    repo_url = project["Url"]

    # Skip if already processed
    if repo_name in selected_projects:
        continue

    print(f"Processing: {repo_name}")
    if fetch_package_lock(repo_url, repo_name):
        print(f"Saved: {repo_name}.json")
        valid_count += 1
    else:
        print(f"No package-lock.json for: {repo_name}")

    selected_projects.add(repo_name)

print(f"Done! Retrieved {valid_count} package-lock.json files.")
