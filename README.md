# Medicine Pricing Project

This project fetches Iceland's medicine pricing over time from their [website](https://www.lyfjastofnun.is). It uses the ngods stack for end-to-end processing.

## Overview

This project demonstrates creating a complete data stack using only open-source tools from ngods.

It leverages the following technologies:

- **Python**: Used for scripting and data processing.
- **dbt**: Handles the transformation of data within the data warehouse.
- **[dagster-dbt](https://docs.dagster.io)**: Orchestrates and schedules the dbt jobs.
- **[DuckDB](https://duckdb.org)**: An in-process SQL OLAP database management system.
- **Minio**: Provides S3-compatible object storage.
- **Cube.js**: Enables data modeling and analytics.
- **Trino**: A distributed SQL query engine for big data analytics.

This stack allows for efficient, scalable, and fully open-source data processing and analysis.

![Growth of wholesale price for selected medicine over the years](images\image.png)

## File Structure

- **.vscode**: VS Code settings.
- **common**: Shared modules and utilities.
- **dagster_etl**: Dagster ETL pipelines.
- **dagster_etl_tests**: Tests for Dagster ETL.
- **dbt_project**: dbt models and configurations.
- **images**: Project-related images.
- **infrastructure**: Infrastructure as code.
- **model**: Data models.
- **example_env**: Environment variable examples.
- **docker-compose.yml**: Docker Compose configuration.
- **Makefile**: Automation tasks.
- **setup.py, pyproject.toml, setup.cfg**: Python package configuration.

## Getting Started

### Prerequisites

- Docker
- Python 3.8+

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Rafno/medicine_pricing.git
   cd medicine_pricing
   ```

2. **Install python and DBT dependencies:**  
    ```
    pip install -e ".[dev]"
    cd dbt_project
	dbt deps 
    ```

3. **Start Dagster UI:**  
    ```
    dagster dev
    ```

4. ***Start Minio and Cuble with Docker Compose:***  
    ```
    docker-compose up
    ```

5. ***Apply Terraform infrastructure:***  
    ```
    cd infrastructure
    terraform apply
    ```
6. ***Open the project in your browser:***  
    localhost:3000 - Dagster  
    localhost:4000 - Cube  
    localhost:9000 - Minio  

### Passwords  
Minio user: youraccesskey  
Minio password: yoursecretkey

This can be changed in docker compose.

## Environment Variables  
Use values directly from example_env, and create a .env file in your project with those values.

## Adding Dependencies  
Specify new dependencies in setup.py.

## Testing  
Run tests using pytest:
```
pytest dagster_etl_tests
```


# Infrastructure
Apache Iceberg: Data storage format (TODO)  
Trino: Federated data query (TODO)  
dbt: ELT  
Dagster: Data orchestration  
Cube.dev: Data analysis and semantic model
Metabase: Self-service data visualization (TODO)  
Minio: Local S3 storage  


## Learn More  
Dagster Tutorials  
dbt + Dagster tutorial  