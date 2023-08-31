import pytest
import os
from pathlib import Path
from flows.ingest import submit_dataproc_job


def test_submit_dataproc_job_successful(mock_dataproc_env, mock_gcp_creds, mock_dataproc_client, mocker):
    """
    This test simulates a successful submitting a Spark job to DataProc Cluster
    Fixtures will be automatically executed before running a test.
    :param mock_dataproc_env: fixture to mock environment variables for DataProc
    :param mock_gcp_creds: fixture to mock the GcpCredentials and its load method
    :param mock_dataproc_client: fixture to mock the dataproc and its JobControllerClient
    """
    # Mock other dependencies
    mocker.patch('uuid.uuid4', return_value='test_uuid')
    mocker.patch('os.getenv', side_effect=lambda x: os.environ.get(x, 'default_value'))

    # Mock the return value of operation.result().reference.job_id
    mock_dataproc_client.submit_job_as_operation.return_value.result.return_value.reference.job_id = 'test_uuid'

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

    # Verify the GcpCredentials block get credentials method was called
    # Assert that the get_credentials_from_service_account method of our mock_gcp_creds object
    # was called exactly once, verifying that get credentials was attempted.
    mock_gcp_creds.get_credentials_from_service_account.assert_called_once()

    # Assert that the submit_job_as_operation method of our mock_dataproc_client object
    # was called
    mock_dataproc_client.submit_job_as_operation.assert_called()
    assert job_id == 'test_uuid'


def test_submit_dataproc_job_exception_handling(mock_dataproc_env, mock_gcp_creds, mock_dataproc_client):
    """
    This test simulates a failure in submitting a Spark job to DataProc Cluster
    """
    # Mock an exception when submit_job_as_operation is called
    mock_dataproc_client.submit_job_as_operation.side_effect = Exception("Test Exception")

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
    assert str(e.value) == "Test Exception"

    # Assert that the submit_job_as_operation method was called
    mock_dataproc_client.submit_job_as_operation.assert_called_once()
