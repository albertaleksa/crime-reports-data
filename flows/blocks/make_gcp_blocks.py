from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
import json
from dotenv import load_dotenv
import os

# alternative to creating GCP blocks in the UI

# values from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../../.env'))

credentials_file_path = os.getenv("GCP_CREDENTIALS_PATH")

credentials_block_name = os.getenv("CREDS_BLOCK_NAME")
bucket_block_name = os.getenv("BUCKET_BLOCK_NAME")
bucket_name = os.getenv("DATA_LAKE_BUCKET_NAME")

with open(credentials_file_path, "r") as f:
    service_account_info = json.load(f)

credentials_block = GcpCredentials(
    service_account_info=service_account_info
)
credentials_block.save(credentials_block_name, overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load(credentials_block_name),
    bucket=bucket_name,
)

bucket_block.save(bucket_block_name, overwrite=True)