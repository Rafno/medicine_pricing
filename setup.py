import glob

from setuptools import find_packages, setup

setup(
    name="dagster_etl",
    packages=find_packages(exclude=["dagster_etl_tests"]),
    # package data paths are relative to the package key
    package_data={
        "dagster_etl": ["../" + path for path in glob.glob("dbt_project/**", recursive=True)]
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster_aws",
        "boto3",
        "dagster-dbt",
        "pandas",
        "beautifulsoup4",
        "scipy",
        "dbt-core",
        "dbt-duckdb",
        "dagster-duckdb",
        "dagster-duckdb-pandas",
        "xlrd", # These are used for converting xls and xlsx
        "openpyxl",
        # packaging v22 has build compatibility issues with dbt as of 2022-12-07
        "packaging<22.0",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
