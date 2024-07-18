from dagster import AssetExecutionContext, asset, MetadataValue, Failure
import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO
from ...utils.constants import MEDS_URL, BUCKET_NAME
from ...utils import add_date_column
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

@asset(
    compute_kind="s3",
    required_resource_keys={"s3"},
)
def download_medicine_pricing_files(context: AssetExecutionContext) -> pd.DataFrame:
    """Download all the files and store in bucket"""
    session = requests.Session()
    response = session.get(MEDS_URL, headers=headers)
    context.log.info(f"Response status code: {response.status_code}")
    file_name_list = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a")

        # Regex pattern to match the required URLs because they keep changing the format
        pattern = re.compile(r"/wp-content/uploads/\d{4}/\d{2}/lyfjaverdskra.*\.xls")
        for link in links:
            href = link.get("href")
            if not pattern.search(href):
                #If we don't match the desired pattern, e.g. any other tag, move on.
                continue

            # Download the file content
            file_response = session.get(href, headers=headers)
            if file_response.status_code == 200:
                # Prepare the file content for upload
                file_content = BytesIO(file_response.content)
                file_key = f"landing/{href.split('/')[-1]}"  # Extract the file name from the URL
                try:
                    # Upload the file content to S3
                    context.resources.s3.upload_fileobj(file_content, BUCKET_NAME, file_key)
                    context.log.info(f"Successfully uploaded {file_key} to {BUCKET_NAME}")
                    file_name_list.append(f'{BUCKET_NAME}/file_key')
                except Exception as e:
                    context.log.error(f"Failed to upload {file_key} to {BUCKET_NAME}: {e}")
                    raise Failure(
                    description=f"Failed to upload {file_key} to {BUCKET_NAME}",
                    metadata={"exception": str(e)}
                    )

        context.add_output_metadata({
            "file_count": MetadataValue.int(len(file_name_list)),
        })
        
    else:
        context.log.error(
            f"Failed to retrieve the webpage. Status code: {response.status_code}"
        )


    return pd.DataFrame(file_name_list, columns=['links']) #To be used in next step.


@asset(required_resource_keys={"s3"})
def stage_pricing(context: AssetExecutionContext) -> pd.DataFrame:
    response = context.resources.s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix='landing'
    )
    # List to store individual DataFrames
    dataframes = []

    # Iterate through each item in the 'Contents' list and download the file
    for content in response.get('Contents', []):
        key = content.get('Key')
        context.log.info(f'Downloading {key}')
        
        # Create an in-memory bytes buffer
        buffer = BytesIO()
        
        # Download the file content to the buffer
        context.resources.s3.download_fileobj(Bucket=BUCKET_NAME, Key=key, Fileobj=buffer)
        
        # Move the pointer to the beginning of the buffer
        buffer.seek(0)
        
        # Read the buffer into a pandas DataFrame
        try:
            # Determine file format by checking the extension
            if key.endswith('.xls'):
                df = pd.read_excel(buffer, engine='xlrd')
            elif key.endswith('.xlsx'):
                df = pd.read_excel(buffer, engine='openpyxl')
            else:
                context.log.error(f'Unsupported file extension for {key}')
                continue
            
            context.log.info(f'Successfully read {key} into a DataFrame')
            
            # Add the DataFrame to the list
            file_name = key.replace('landing/', '')
            df = df.assign(file_name=file_name)
            df = add_date_column(df=df, filename=file_name)
            dataframes.append(df)

        except Exception as e:
            context.log.error(f'Error reading {key} into a DataFrame: {e}')
            raise Failure

    # Concatenate all DataFrames into a single composite DataFrame
    composite_df = pd.concat(dataframes, ignore_index=True)

    # Optionally, log or return the composite DataFrame
    context.log.info('Successfully created composite DataFrame')
    return composite_df