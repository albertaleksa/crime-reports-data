import pytest
import requests
import os
from pathlib import Path
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from google.cloud import dataproc_v1 as dataproc


@pytest.fixture
def url():
    """
    This fixture returns the url used in tests.
    """
    return "http://url"


@pytest.fixture
def csv_name():
    """
    This fixture returns the name of the CSV file used in tests.
    """
    return "aus_test_file.csv"


@pytest.fixture
def mock_content():
    """
    This fixture returns the mock content for a successful download.
    """
    return b"some,data,here\nanother,row,here"


@pytest.fixture()
def file_path():
    """
    This fixture returns the paths of the CSV files used in tests.
    """
    from_path = Path('data/test_file.csv')
    to_path = Path('gcs/test_file.csv')

    dict_path = {
        "from_path": from_path,
        "to_path": to_path
    }

    return dict_path


@pytest.fixture
def mock_requests_get(mocker):
    """
    This fixture mocks the `requests.get` method.
    """
    mock = mocker.MagicMock()
    mocker.patch.object(requests, "get", return_value=mock)
    return mock


@pytest.fixture
def mock_successful_download(mock_requests_get, mock_content):
    """
    This fixture simulates a successful file download.
    """
    # Mock the requests.get response
    mock_requests_get.status_code = 200
    # Mock the content of the file
    mock_requests_get.iter_content.return_value = [mock_content]
    return mock_content


@pytest.fixture
def mock_failed_download(mock_requests_get):
    """
    This fixture simulates a failed download
    by making the mocked request return a 404 status code.
    """
    mock_requests_get.status_code = 404


@pytest.fixture
def mock_env(mocker):
    """
    This fixture mocks environment variables BUCKET_BLOCK_NAME and SPARK_JOB_FILE
    """
    env_vars = {
        "BUCKET_BLOCK_NAME": "test_bucket",
        "SPARK_JOB_FILE": "spark_job.py"
    }
    mocker.patch.dict(os.environ, env_vars)


@pytest.fixture
def mock_dataproc_env(mocker):
    """
    This fixture mocks environment variables for DataProc
    """
    env_vars = {
        "PROJECT_ID": "test_project",
        "REGION": "test_region",
        "DATAPROC_CLUSTER_NAME": "test_cluster",
        "DATA_LAKE_BUCKET_NAME": "test_bucket",
        "CREDS_BLOCK_NAME": "test_creds"
    }
    mocker.patch.dict(os.environ, env_vars)


@pytest.fixture
def mock_os(mocker):
    """
    This fixture mocks `os.path.exists`
    """
    # Mock os.remove to prevent the test from actually deleting any files.
    mocker.patch('os.remove')
    # Mock os.path.exists to always return True,
    # simulating that the file to be uploaded does exist.
    mocker.patch('os.path.exists', return_value=True)


@pytest.fixture
def assert_env_vars():
    """
    This fixture returns a function that assert that the env variables match the .env file
    """
    def _assert_env_vars_match_file(env_path):
        # Open the .env file
        with open(env_path, 'r') as file:
            for line in file:
                # Skip comments and empty lines
                if line.startswith('#') or line.strip() == '':
                    continue

                # Split the line into key and value
                key, value = line.strip().split('=', 1)

                # Remove quotes if present
                value = value.strip('"')

                # Substitute references to other environment variables
                if '${' in value:
                    var_name = value[value.index('${') + 2: value.index('}')]
                    value = value.replace('${' + var_name + '}', os.getenv(var_name))

                # Check that the environment variable matches the value in the file
                assert os.getenv(key) == value

    return _assert_env_vars_match_file


# Fixtures for GcpCredentials
@pytest.fixture
def mock_gcp_credentials(mocker):
    """
    This fixture mocks the GcpCredentials.
    """
    # Create a mock object using Python's MagicMock.
    # This mock will be used to simulate the behavior of the GcpCredentials
    mocked_gcp_credentials = mocker.MagicMock(spec=GcpCredentials)
    return mocked_gcp_credentials


@pytest.fixture
def mock_gcp_credentials_load(mocker, mock_gcp_credentials):
    """
    This fixture mocks the GcpCredentials load method.
    """
    # Mock the GcpCredentials.load method to return our mock_gcs object
    # instead of actually interacting with the GcpCredentials.
    mocked_gcp_credentials_load = mocker.patch("prefect_gcp.GcpCredentials.load", return_value=mock_gcp_credentials)
    return mocked_gcp_credentials_load


@pytest.fixture
def mock_gcp_credentials_block(mocker, mock_gcp_credentials):
    """
    This fixture mocks the GcpCredentials block creation.
    """
    # Mock the instance creation of the GcpCredentials object.
    mocked_gcp_credentials_block = mocker.patch(
        "flows.blocks.make_gcp_blocks.GcpCredentials",
        return_value=mock_gcp_credentials
    )
    return mocked_gcp_credentials_block


# Fixtures for GcsBucket
@pytest.fixture
def mock_gcs_bucket(mocker):
    """
    This fixture mocks the GcsBucket.
    """
    # Create a mock object using Python's MagicMock.
    # This mock will be used to simulate the behavior of the GCS bucket
    mocked_gcs_bucket = mocker.MagicMock(spec=GcsBucket)
    return mocked_gcs_bucket


@pytest.fixture
def mock_gcs_bucket_load(mocker, mock_gcs_bucket):
    """
    This fixture mocks the GcsBucket load method.
    """
    # Mock the GcsBucket.load method to return our mock_gcs object
    # instead of actually interacting with the GCS bucket.
    mocked_gcs_bucket_load = mocker.patch("prefect_gcp.cloud_storage.GcsBucket.load", return_value=mock_gcs_bucket)
    return mocked_gcs_bucket_load


@pytest.fixture
def mock_gcs_bucket_block(mocker, mock_gcs_bucket):
    """
    This fixture mocks the GcsBucket block creation.
    """
    # Mock the instance creation of the GcsBucket object.
    mocked_gcs_bucket_block = mocker.patch("flows.blocks.make_gcp_blocks.GcsBucket", return_value=mock_gcs_bucket)
    return mocked_gcs_bucket_block


# Fixtures for dataproc.JobControllerClient
@pytest.fixture
def mock_job_controller_client(mocker):
    """
    This fixture mocks the JobControllerClient.
    """
    # Create a mock object using Python's MagicMock.
    # This mock will be used to simulate the behavior of the JobControllerClient
    mocked_job_controller_client = mocker.MagicMock(spec=dataproc.JobControllerClient)
    return mocked_job_controller_client


@pytest.fixture
def mock_dataproc_client(mocker, mock_job_controller_client):
    """
    This fixture mocks the DataProc client creation.
    """
    # Mock the instance creation of the JobControllerClient object.
    mocked_dataproc_client = mocker.patch(
        "google.cloud.dataproc_v1.JobControllerClient",
        return_value=mock_job_controller_client
    )
    return mocked_dataproc_client
