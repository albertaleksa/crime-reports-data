import pytest
import requests
import os
from pathlib import Path


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
def mock_gcs(mocker):
    """
    This fixture mocks the GcsBucket and its load method.
    """
    # Create a mock object using Python's MagicMock.
    # This mock will be used to simulate the behavior of the GCS bucket
    mock = mocker.MagicMock()
    # Mock the GcsBucket.load method to return our mock_gcs object
    # instead of actually interacting with the GCS bucket.
    mocker.patch('prefect_gcp.cloud_storage.GcsBucket.load', return_value=mock)
    return mock


@pytest.fixture
def mock_gcp_creds_in_make_gcp_blocks(mocker):
    """
    TThis fixture mocks the GcpCredentials in make_gcp_blocks.
    """
    # Mock GcpCredentials
    mocked_gcp_credentials = mocker.MagicMock()
    mocker.patch('flows.blocks.make_gcp_blocks.GcpCredentials', return_value=mocked_gcp_credentials)
    return mocked_gcp_credentials


# @pytest.fixture
# def mock_gcp_cred_base(mocker):
#     """
#     This fixture mocks the GcpCredentials.
#     """
#     mock = mocker.MagicMock()
#     mocker.patch('flows.ingest.GcpCredentials', return_value=mock)
#     return mock


# @pytest.fixture
# def mock_gcp_creds(mock_gcp_cred_base, mocker):
#     """
#     This fixture builds upon mock_gcp_credentials to additionally mock the load() method.
#     """
#     # mock_load = mocker.patch.object(mock_gcp_cred_base, 'load')
#     mock_load = mocker.patch.object(mock_gcp_cred_base, 'load', new=mocker.MagicMock())
#     # mock_gcp_cred_base.load = mock_load
#     return mock_load


@pytest.fixture
def mock_gcp_creds(mocker):
    """
    This fixture builds upon mock_gcp_credentials to additionally mock the load() method.
    """
    mock = mocker.MagicMock()
    mocker.patch('prefect_gcp.GcpCredentials.load', return_value=mock)
    return mock


@pytest.fixture
def mock_dataproc_client(mocker):
    """
    This fixture mocks the dataproc and its JobControllerClient.
    """
    mock = mocker.MagicMock()
    mocker.patch('google.cloud.dataproc_v1.JobControllerClient', return_value=mock)
    return mock


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
