import pytest
import os
from pathlib import Path
from flows.ingest import submit_dataproc_job


def test_submit_dataproc_job_successful(mocker,
                                        mock_dataproc_env,
                                        mock_gcp_credentials,
                                        mock_gcp_credentials_load,
                                        mock_job_controller_client,
                                        mock_dataproc_client):
    """
    This test simulates a successful submitting a Spark job to DataProc Cluster
    Fixtures will be automatically executed before running a test.
    :param mock_dataproc_env: fixture to mock environment variables for DataProc
    :param mock_gcp_credentials: fixture to mock the GcpCredentials
    :param mock_gcp_credentials_load: fixture to mock the GcpCredentials load method
    :param mock_job_controller_client: fixture to mock the JobControllerClient.
    :param mock_dataproc_client: fixture to mock the DataProc client creation.
    """
    # Mock other dependencies
    mock_job_id = "test_uuid"
    mocker.patch("uuid.uuid4", return_value=mock_job_id)
    mocker.patch("os.getenv", side_effect=lambda x, default=None: os.environ.get(x, f"test_{x.lower()}"))
    mocked_credentials = "mocked_credentials"

    # Mock the get_credentials_from_service_account method of the MagicMock returned by GcpCredentials.load
    mock_gcp_credentials.get_credentials_from_service_account.return_value = mocked_credentials

    # Mock the submit_job_as_operation method to return a mock operation object
    mock_operation = mocker.MagicMock()
    mock_operation.result.return_value = mocker.MagicMock(reference=mocker.MagicMock(job_id=mock_job_id))
    mock_job_controller_client.submit_job_as_operation.return_value = mock_operation

    # Define test input arguments
    spark_job_file = Path("test_spark_job.py")
    temp_gcs_bucket = "temp_gcs_bucket"
    input_path_aus = "input_path_aus"
    output_path_aus = "output_path_aus"
    output_bq_aus = "output_bq_aus"
    input_path_la = "input_path_la"
    output_path_la = "output_path_la"
    output_bq_la = "output_bq_la"
    input_path_sd = "input_path_sd"
    output_path_sd = "output_path_sd"
    output_bq_sd = "output_bq_sd"

    # Define test expected job details for the PySpark job
    expected_job_details = {
        "reference": {"job_id": mock_job_id},
        "placement": {"cluster_name": os.getenv("DATAPROC_CLUSTER_NAME")},
        "pyspark_job": {
            "main_python_file_uri": f"gs://{os.getenv('DATA_LAKE_BUCKET_NAME')}/{spark_job_file}",
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

    # Call the function
    job_id = submit_dataproc_job.fn(
        spark_job_file,
        temp_gcs_bucket,
        input_path_aus,
        output_path_aus,
        output_bq_aus,
        input_path_la,
        output_path_la,
        output_bq_la,
        input_path_sd,
        output_path_sd,
        output_bq_sd
    )

    # Assertions
    # Check if GcpCredentials.load was called
    mock_gcp_credentials_load.assert_called_once_with(os.getenv("CREDS_BLOCK_NAME"))

    # Check if the mocked method get_credentials_from_service_account was called as expected
    mock_gcp_credentials.get_credentials_from_service_account.assert_called_once()

    # Check if JobControllerClient was instantiated with the correct arguments
    mock_dataproc_client.assert_called_once_with(
        credentials=mocked_credentials,
        client_options={"api_endpoint": f"{os.getenv('REGION')}-dataproc.googleapis.com:443"}
    )

    # Check if submit_job_as_operation method was called with the correct arguments
    mock_job_controller_client.submit_job_as_operation.assert_called_once_with(
        request={
            "project_id": os.getenv("PROJECT_ID"),
            "region": os.getenv("REGION"),
            "job": expected_job_details
        }
    )

    assert job_id == mock_job_id


def test_submit_dataproc_job_exception_handling(mocker,
                                                mock_dataproc_env,
                                                mock_gcp_credentials,
                                                mock_gcp_credentials_load,
                                                mock_job_controller_client,
                                                mock_dataproc_client):
    """
    This test simulates a failure in submitting a Spark job to DataProc Cluster
    """
    # Mock other dependencies
    mock_job_id = "test_uuid"
    mocker.patch("uuid.uuid4", return_value=mock_job_id)
    mocker.patch("os.getenv", side_effect=lambda x, default=None: os.environ.get(x, f"test_{x.lower()}"))
    mocked_credentials = "mocked_credentials"

    # Mock the get_credentials_from_service_account method of the MagicMock returned by GcpCredentials.load
    mock_gcp_credentials.get_credentials_from_service_account.return_value = mocked_credentials

    # Mock an exception when submit_job_as_operation is called
    mock_job_controller_client.submit_job_as_operation.side_effect = Exception("Test Exception")

    # Define test input arguments
    spark_job_file = "test_spark_job.py"
    temp_gcs_bucket = "temp_gcs_bucket"
    input_path_aus = "input_path_aus"
    output_path_aus = "output_path_aus"
    output_bq_aus = "output_bq_aus"
    input_path_la = "input_path_la"
    output_path_la = "output_path_la"
    output_bq_la = "output_bq_la"
    input_path_sd = "input_path_sd"
    output_path_sd = "output_path_sd"
    output_bq_sd = "output_bq_sd"

    # Call the function and assert it raises the expected exception
    with pytest.raises(Exception) as e:
        submit_dataproc_job.fn(
            spark_job_file,
            temp_gcs_bucket,
            input_path_aus,
            output_path_aus,
            output_bq_aus,
            input_path_la,
            output_path_la,
            output_bq_la,
            input_path_sd,
            output_path_sd,
            output_bq_sd
        )

    # Assertions
    # Check if GcpCredentials.load was called
    mock_gcp_credentials_load.assert_called_once_with(os.getenv("CREDS_BLOCK_NAME"))

    # Check if the mocked method get_credentials_from_service_account was called as expected
    mock_gcp_credentials.get_credentials_from_service_account.assert_called_once()

    # Check if JobControllerClient was instantiated with the correct arguments
    mock_dataproc_client.assert_called_once_with(
        credentials=mocked_credentials,
        client_options={"api_endpoint": f"{os.getenv('REGION')}-dataproc.googleapis.com:443"}
    )

    # Check if submit_job_as_operation method was called once with the correct arguments
    mock_job_controller_client.submit_job_as_operation.assert_called_once()

    assert str(e.value) == "Test Exception"
