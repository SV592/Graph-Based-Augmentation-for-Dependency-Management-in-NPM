# Dependency Management Graph Scripts

This repository provides Python scripts to analyze and visualize dependency relationships in `package-lock.json` files from NPM projects. It includes tools for data collection, parsing, graph construction, and querying. Below is an overview of the scripts and their usage.

---

## Table of Contents
- [Scripts Overview](#scripts-overview)
  - [get_package_lock_files.py](#1-get_package_lock_filespy)
  - [parser_v1.py](#2-parser_v1py)
  - [parser_v2.py](#3-parser_v2py)
  - [automate_data_collection.py](#4-automate_data_collectionpy)
  - [knowledge_graph.py](#5-knowledge_graphpy)
  - [query_graph.py](#6-query_graphpy)
- [Environment Setup](#environment-setup)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
- [Execution Workflow](#execution-workflow)
- [Contribution](#contribution)
- [License](#license)

---

## Execution Workflow

### 1. `get_package_lock_files.py`
- **Purpose**: Automates collection of `package-lock.json` files from GitHub repositories.
- **Features**:
  - Fetches repositories using the GitHub API.
  - Organizes downloaded files into a structured directory.
- **Usage**:
  - Configure GitHub token and search parameters in the script.
  - Run to download package-lock files.
- **Output**: Collected `package-lock.json` files in a designated folder.

---

### 2. `parser_v1.py`
- **Purpose**: Parses `package-lock.json` files of version 1.
- **Features**:
  - Processes dependencies and outputs them in a structured format.
- **Usage**:
  - Specify input and output directories in the script.
  - Run to parse all version 1 files.
- **Output**: Parsed dependency data in JSON format.

---

### 3. `parser_v2.py`
- **Purpose**: Parses `package-lock.json` files of version 2.
- **Features**:
  - Handles nested dependencies.
  - Extracts types like `peerDependencies` and `optionalDependencies`.
- **Usage**:
  - Set input and output directories.
  - Run to parse version 2 lock files.
- **Output**: Parsed dependency data in JSON format.

---

### 4. `automate_data_collection.py`
- **Purpose**: Filters projects based on criteria like downloads and commits.
- **Features**:
  - Uses Libraries.io and GitHub APIs.
  - Filters based on download count (≥1000) and commit count (≥700).
- **Usage**:
  - Configure API keys and thresholds in the script.
  - Run to retrieve filtered project metadata.
- **Output**: Metadata for selected projects.

---

### 5. `knowledge_graph.py`
- **Purpose**: Builds a dependency graph in Neo4j from parsed JSON files.
- **Features**:
  - Creates nodes for each package with properties.
  - Establishes edges for dependency relationships.
- **Usage**:
  - Configure Neo4j connection details.
  - Run to construct the dependency graph.
- **Output**: Dependency graph in a Neo4j database.

---

### 6. `query_graph.py`
- **Purpose**: Queries the Neo4j dependency graph to analyze properties.
- **Features**:
  - Predefined Cypher queries for metrics like graph density and unused dependencies.
- **Usage**:
  - Execute after constructing the graph with `knowledge_graph.py`.
  - Configure output paths for results.
- **Output**: Query results as CSV files or terminal output.

---

## Environment Setup

### Dependencies
- **Python Packages**: `py2neo`, `pandas`, `tqdm`, `matplotlib`
- **Database**: Neo4j Community Edition (or above)
- **APIs**: GitHub API 

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/SV592/CS848-Fall2024-Shaquille
   cd CS848-Fall2024-Shaquille
