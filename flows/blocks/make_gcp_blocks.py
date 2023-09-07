from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
import json
from dotenv import load_dotenv
import os


def load_and_get_environment_variables(env_path=None) -> dict:
    """
    Load .env file with environment variables
    and return some of them to use for creating GCP cred block and GCP storage block
    :return: dictionary of env vars
    """
    # Load values from .env file
    if env_path is None:
        basedir = os.path.abspath(os.path.dirname(__file__))
        env_path = os.path.join(basedir, '../../.env')

    res = load_dotenv(env_path)

    if res:
        print("File with environment variables was successfully loaded.")
    else:
        print("Error loading the file with environment variables.")

    # Get and return environment variables
    env_vars = {
        "credentials_file_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        "credentials_block_name": os.getenv("CREDS_BLOCK_NAME"),
        "bucket_name": os.getenv("DATA_LAKE_BUCKET_NAME"),
        "bucket_block_name": os.getenv("BUCKET_BLOCK_NAME")
    }
    return env_vars


def create_gcp_credentials_block(credentials_file_path: str, credentials_block_name: str) -> None:
    """
    Create GCP credential block
    :param credentials_file_path: path to service account credential file
    :param credentials_block_name: name for GCP credential block
    """
    with open(credentials_file_path, "r") as f:
        service_account_info = json.load(f)

    credentials_block = GcpCredentials(
        service_account_info=service_account_info
    )
    credentials_block.save(credentials_block_name, overwrite=True)

    return


def create_gcp_bucket_block(credentials_block_name: str, bucket_name: str, bucket_block_name: str) -> None:
    """
    Create GCP bucket block
    :param credentials_block_name: name of the GCP credential block
    :param bucket_name: the name of the storage (bucket) in GCP
    :param bucket_block_name: name for GCP bucket block
    """
    gcp_credentials_block = GcpCredentials.load(credentials_block_name)

    bucket_block = GcsBucket(
        gcp_credentials=gcp_credentials_block,
        bucket=bucket_name,
    )
    bucket_block.save(bucket_block_name, overwrite=True)

    return


# alternative to creating GCP blocks in the UI
def main():
    # # values from .env file
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # load_dotenv(os.path.join(basedir, '../../.env'))
    #
    # credentials_file_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    #
    # credentials_block_name = os.getenv("CREDS_BLOCK_NAME")
    # bucket_name = os.getenv("DATA_LAKE_BUCKET_NAME")
    # bucket_block_name = os.getenv("BUCKET_BLOCK_NAME")

    # with open(credentials_file_path, "r") as f:
    #     service_account_info = json.load(f)
    #
    # credentials_block = GcpCredentials(
    #     service_account_info=service_account_info
    # )
    # credentials_block.save(credentials_block_name, overwrite=True)

    # bucket_block = GcsBucket(
    #     gcp_credentials=GcpCredentials.load(credentials_block_name),
    #     bucket=bucket_name,
    # )
    #
    # bucket_block.save(bucket_block_name, overwrite=True)

    env_vars = load_and_get_environment_variables()

    create_gcp_credentials_block(
        credentials_file_path=env_vars["credentials_file_path"],
        credentials_block_name=env_vars["credentials_block_name"]
    )

    create_gcp_bucket_block(
        credentials_block_name=env_vars["credentials_block_name"],
        bucket_name=env_vars["bucket_name"],
        bucket_block_name=env_vars["bucket_block_name"]
    )


if __name__ == '__main__':
    main()
