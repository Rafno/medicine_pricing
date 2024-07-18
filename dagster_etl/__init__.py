import os

from dagster import (
    Definitions,
    FilesystemIOManager,
    load_assets_from_package_module,
)
from dagster_duckdb_pandas import DuckDBPandasIOManager
from dagster_aws.s3 import S3PickleIOManager, s3_resource

from .assets import raw_data
from .assets.dbt import DBT_PROJECT_DIR, dbt_project_assets, dbt_resource
from .resources import my_s3_resource

raw_data_assets = load_assets_from_package_module(
    raw_data,
    group_name="raw_data",
    # all of these assets live in the duckdb database, under the schema raw_data
    key_prefix=["raw_data"],
)


# forecasting_freshness_checks = build_last_update_freshness_checks(
#     assets=[predicted_orders],
#     lower_bound_delta=datetime.timedelta(days=2),
# )


resources = {
    # this io_manager allows us to load dbt models as pandas dataframes
    "io_manager": DuckDBPandasIOManager(database=os.path.join(DBT_PROJECT_DIR, "medicines.duckdb")),
    "s3_io_manager": S3PickleIOManager(
            s3_resource=my_s3_resource,
            s3_bucket="staging",
            s3_prefix="raw_data",
    ),
    "s3": my_s3_resource,
    # this io_manager is responsible for storing/loading our pickled machine learning model
    "model_io_manager": FilesystemIOManager(),
    # this resource is used to execute dbt cli commands
    "dbt": dbt_resource,
}

defs = Definitions(
    assets=[dbt_project_assets, *raw_data_assets],
    resources=resources,
)
