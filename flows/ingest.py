import argparse
import sys
import requests
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import uuid
import pandas as pd

from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_gcp.cloud_storage import GcsBucket
# use GCP Credentials block for storing credentials
from prefect_gcp import GcpCredentials

from google.cloud import storage
from google.cloud import dataproc_v1 as dataproc


# @task(log_prints=True, retries=3, retry_delay_seconds=60, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
@task(log_prints=True, retries=3, retry_delay_seconds=60)
def download_file(url: str, csv_name: str) -> Path:
    """Download data from web into local storage"""
    city = csv_name.split("_")[0]
    path = Path(f"data/{city}/{csv_name}")
    print(f"Downloading file {csv_name} for {city}")

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
        print(f"File {csv_name} downloaded successfully. Full size is {downloaded_size_mb:.2f} MB")
    else:
        print("Error downloading the file.")
    return path


@task(log_prints=True)
def upload_to_gcs(path: Path) -> None:
    """Upload local file to GCS"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '../.env'))
    bucket_block_name = os.getenv("BUCKET_BLOCK_NAME")
    gcs_block = GcsBucket.load(bucket_block_name)
    path_1 = path.parts[0]
    path_rest = "/".join(path.parts[1:])

    # Check if the file exists
    if os.path.exists(path):
        # If the file exists, upload it to GCS
        gcs_block.upload_from_path(from_path=f"{path}", to_path=f"{path_1}/raw/{path_rest}", timeout=300)
        os.remove(path)
    else:
        print(f"The file '{path}' does not exist.")

    return


@task(log_prints=True)
def upload_job_to_gcs() -> Path:
    """Upload python-file with Spark job to gcs"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '../.env'))

    bucket_block_name = os.getenv("BUCKET_BLOCK_NAME")
    spark_job_file = os.getenv("SPARK_JOB_FILE")
    spark_job_file_path = f'flows/{os.getenv("SPARK_JOB_FILE")}'
    gcs_block = GcsBucket.load(bucket_block_name)
    path = Path(f"code/{spark_job_file}")

    # Check if the file exists
    if os.path.exists(spark_job_file_path):
        # If the file exists, upload it to GCS
        gcs_block.upload_from_path(from_path=spark_job_file_path, to_path=path, timeout=300)
    else:
        print(f"The file '{spark_job_file_path}' does not exist.")

    return path


@task(log_prints=True)
def submit_dataproc_job(spark_job_file: Path, temp_gcs_bucket: str,
                        input_path_aus: str, output_path_aus: str, output_bq_aus: str,
                        input_path_la: str, output_path_la: str, output_bq_la: str,
                        input_path_sd: str, output_path_sd: str, output_bq_sd: str):
    """Submit Spark job to DataProc Cluster"""
    project_id = os.getenv("PROJECT_ID")
    region = os.getenv("REGION")
    cluster_name = os.getenv("DATAPROC_CLUSTER_NAME")
    bucket_name = os.getenv("DATA_LAKE_BUCKET_NAME")

    # Use Prefect GcpCredentials Block which stores credentials
    credentials_block_name = os.getenv("CREDS_BLOCK_NAME")
    gcp_credentials_block = GcpCredentials.load(credentials_block_name)
    credentials = gcp_credentials_block.get_credentials_from_service_account()

    # Set up DataProc client and cluster information
    dataproc_client = dataproc.JobControllerClient(
        credentials=credentials,
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(region)}
    )

    # Define the PySpark job
    job_details = {
        "reference": {"job_id": str(uuid.uuid4())},
        "placement": {"cluster_name": cluster_name},
        "pyspark_job": {
            "main_python_file_uri": f"gs://{bucket_name}/{spark_job_file}",
            # "args": [input_file, output_file],
            "args": [
                "--temp_gcs_bucket", temp_gcs_bucket,
                "--input_path_aus", input_path_aus,
                "--output_path_aus", output_path_aus,
                "--output_bq_aus", output_bq_aus,
                "--input_path_la", input_path_la,
                "--output_path_la", output_path_la,
                "--output_bq_la", output_bq_la,
                "--input_path_sd", input_path_sd,
                "--output_path_sd", output_path_sd,
                "--output_bq_sd", output_bq_sd
            ],
            "jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"],
            "python_file_uris": [],
            "file_uris": [],
            "archive_uris": [],
        },
    }

    print(f"job_details = {job_details}")

    # Submit the job
    operation = dataproc_client.submit_job_as_operation(
        request={
            "project_id": project_id,
            "region": region,
            "job": job_details
        }
    )
    response = operation.result()
    print(f"response = {response}")
    print(f"response.reference.job_id = {response.reference.job_id}")

    # Return the job ID
    return response.reference.job_id


@flow(name="Ingest Flow")
def web_to_gcs(url: str, csv_name: str) -> None:
    """Download data in csv and upload to GCS"""
    downloaded_file = download_file(url, csv_name)
    upload_to_gcs(downloaded_file)


@flow(name="Submit Spark Job")
def submit_job(temp_gcs_bucket: str,
               input_path_aus: str, output_path_aus: str, output_bq_aus: str,
               input_path_la: str, output_path_la: str, output_bq_la: str,
               input_path_sd: str, output_path_sd: str, output_bq_sd: str) -> None:
    """Upload spark-job file to GCS and submit this job to DataProc Cluster"""
    # upload python-file with Spark job to gcs
    spark_job_file = upload_job_to_gcs()
    # submit spark job to DataProc Cluster
    submit_dataproc_job(spark_job_file, temp_gcs_bucket,
                        input_path_aus, output_path_aus, output_bq_aus,
                        input_path_la, output_path_la, output_bq_la,
                        input_path_sd, output_path_sd, output_bq_sd)


@flow()
def parent_flow(aus_url: str, la_url_1: str, la_url_2: str, sd_url: str,
                temp_gcs_bucket: str,
                input_path_aus: str, output_path_aus: str, output_bq_aus: str,
                input_path_la: str, output_path_la: str, output_bq_la: str,
                input_path_sd: str, output_path_sd: str, output_bq_sd: str):

    # load data for Austin
    web_to_gcs(aus_url, "aus_2003_2023.csv")

    # load data for Los Angeles
    web_to_gcs(la_url_1, "la_2010_2019.csv")
    web_to_gcs(la_url_2, "la_2020_2023.csv")

    # load data for San Diego
    for year in range(2015, 2024):
        if year < 2018:
            sd_url_full = f"{sd_url}_{year}_datasd_v1.csv"
        else:
            sd_url_full = f"{sd_url}_{year}_datasd.csv"
        web_to_gcs(sd_url_full, f"sd_{year}.csv")
    submit_job(temp_gcs_bucket, input_path_aus, output_path_aus, output_bq_aus,
               input_path_la, output_path_la, output_bq_la,
               input_path_sd, output_path_sd, output_bq_sd)


if __name__ == '__main__':
    aus_url = "<aus_url_path>"
    la_url_1 = "<la_url_path_1>"
    la_url_2 = "<la_url_path_2>"
    sd_url = "<sd_url_path>"

    temp_gcs_bucket = "<temp_gcs_bucket>"
    input_path_aus = "<aus_input_path_gs>"
    output_path_aus = "<aus_ouput_path_gs>"
    output_bq_aus = "<aus_bq_table>"

    input_path_la = "<la_input_path_gs>"
    output_path_la = "<la_ouput_path_gs>"
    output_bq_la = "<la_bq_table>"

    input_path_sd = "<sd_input_path_gs>"
    output_path_sd = "<sd_ouput_path_gs>"
    output_bq_sd = "<sd_bq_table>"

    parent_flow(aus_url, la_url_1, la_url_2, sd_url,
                temp_gcs_bucket, input_path_aus, output_path_aus, output_bq_aus,
                input_path_la, output_path_la, output_bq_la,
                input_path_sd, output_path_sd, output_bq_sd)
