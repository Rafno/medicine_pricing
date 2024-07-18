from dagster_etl.assets.raw_data import meds
from dagster import build_op_context


def test_meds():
    # Define the partition key you want to test
    partition_key = "2020-01-01"
    
    # Build the context with the partition key
    context = build_op_context(
        partition_key=partition_key,
    )
    
    # Call the asset with the context
    meds(context)

# Run the test
test_meds()