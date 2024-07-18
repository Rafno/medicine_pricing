from dagster_aws.s3 import S3Resource

my_s3_resource = S3Resource(
    region_name="us-west-1",
    use_unsigned_session=True,
    endpoint_url="http://localhost:9000",
    use_ssl=False,
)