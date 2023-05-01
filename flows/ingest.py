import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from prefect import flow, task
import requests
from google.cloud import storage
import os
import pandas as pd
from prefect.tasks import task_input_hash
from datetime import timedelta

from prefect_gcp.cloud_storage import GcsBucket


@task(log_prints=True, retries=3, retry_delay_seconds=60, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def download_file(url: str, csv_name: str) -> Path:
    """Download data from web into local storage"""
    city = csv_name.split("_")[0]
    path = Path(f"data/{city}/{csv_name}")

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        downloaded_size = 0
        size = 0
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    downloaded_size_mb = downloaded_size / (1024 * 1024)

                    if int(downloaded_size_mb) % 5 == 0 and size != int(downloaded_size_mb):
                        print(f"\rDownloaded size: {int(downloaded_size_mb)} MB", end="")
                        size = int(downloaded_size_mb)
        print(f"\nFile {csv_name} downloaded successfully. Full size is {downloaded_size_mb:.2f} MB")
    else:
        print("\nError downloading the file.")
    return path


@task(log_prints=True)
def upload_to_gcs(path: Path) -> None:
    """Upload local file to GCS"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '../.env'))
    bucket_block_name = os.getenv("BUCKET_BLOCK_NAME")
    gcs_block = GcsBucket.load(bucket_block_name)

    # Check if the file exists
    if os.path.exists(path):
        # If the file exists, upload it to GCS
        gcs_block.upload_from_path(from_path=path, to_path=f"raw/{path}", timeout=300)
        os.remove(path)
    else:
        print(f"The file '{path}' does not exist.")

    return


@task(log_prints=True)
def upload_job_to_gcs() -> None:
    """Upload python-file with Spark job to gcs"""
    bucket_block_name = os.getenv("BUCKET_BLOCK_NAME")
    spark_job_file = os.getenv("SPARK_JOB_FILE")
    spark_job_file_path = f'flows/{os.getenv("SPARK_JOB_FILE")}'
    gcs_block = GcsBucket.load(bucket_block_name)

    # Check if the file exists
    if os.path.exists(spark_job_file_path):
        # If the file exists, upload it to GCS
        gcs_block.upload_from_path(from_path=spark_job_file_path, to_path=f"code/{spark_job_file}", timeout=300)
    else:
        print(f"The file '{spark_job_file_path}' does not exist.")

    return


@flow(name="Ingest Flow")
def web_to_gcs(url: str, csv_name: str) -> None:
    # download the csv
    downloaded_file = download_file(url, csv_name)
    upload_to_gcs(downloaded_file)
    # upload python-file with Spark job to gcs
    upload_job_to_gcs()



@flow()
def parent_flow():
    # aus_url = "https://data.austintexas.gov/api/views/fdj4-gpfu/rows.csv"
    # la_url_1 = "https://data.lacity.org/api/views/63jg-8b9z/rows.csv"
    # la_url_2 = "https://data.lacity.org/api/views/2nrs-mtv8/rows.csv"
    # # load data for Austin
    # web_to_gcs(aus_url, "aus_2003_2023.csv")
    # # load data for Los Angeles
    # web_to_gcs(la_url_1, "la_2010_2019.csv")
    # web_to_gcs(la_url_2, "la_2020_2023.csv")
    # load data for San Diego
    for year in range(2023, 2024):
        if year < 2018:
            sd_url = f"https://seshat.datasd.org/pd/pd_calls_for_service_{year}_datasd_v1.csv"
        else:
            sd_url = f"https://seshat.datasd.org/pd/pd_calls_for_service_{year}_datasd.csv"
        web_to_gcs(sd_url, f"sd_{year}.csv")


if __name__ == '__main__':
    parent_flow()
    # # Save the original command-line arguments
    # original_argv = sys.argv
    # # Simulate command-line arguments by modifying sys.argv
    # sys.argv = ['pipeline.py',
    #             '--url', 'https://data.lacity.org/api/views/2nrs-mtv8/rows.csv',
    #             '--output_name', 'la_2020_now.csv',
    #             '--bucket_name', 'crime_trends_explorer_data_lake']
    #
    # parser = argparse.ArgumentParser(description='Load csv data')
    # parser.add_argument('--url', type=str, help='url of the csv file')
    # parser.add_argument('--output_name', type=str, help='output name for the csv file')
    # parser.add_argument('--bucket_name', type=str, help='bucket name in gcs for the csv file')
    # args = parser.parse_args()
    #
    #
    # main_flow(args)
    #
    # # Restore the original command-line arguments
    # sys.argv = original_argv

