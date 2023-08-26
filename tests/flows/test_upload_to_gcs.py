import pytest
import os
from pathlib import Path
from flows.ingest import upload_to_gcs


@pytest.fixture
def mock_env(mocker):
    """
    This fixture mocks environment variable BUCKET_BLOCK_NAME
    """
    mocker.patch.dict(os.environ, {'BUCKET_BLOCK_NAME': 'test_bucket'})


@pytest.fixture
def mock_os(mocker):
    """
    This fixture mocks `os.remove` and `os.path.exists`
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


def test_upload_to_gcs_successful(mock_env, mock_os, mock_gcs):
    """
    This test simulates a successful upload to GCS.
    Fixtures will be automatically executed before running a test.
    :param mock_env: fixture to mock environment variable
    :param mock_os: fixture to mock `os.remove` and `os.path.exists`
    :param mock_gcs: fixture to mock the GcsBucket and its load method
    """
    # Define the parameter
    path = Path('data/test_file.csv')

    # Call the function upload_to_gcs with the defined path.
    # Because we've mocked relevant parts of the code,
    # no actual uploading or file manipulation happens.
    upload_to_gcs.fn(path)

    # Verify the GCS upload method was called
    # Assert that the upload_from_path method of our mock_gcs object
    # was called exactly once, verifying that the upload was attempted.
    mock_gcs.upload_from_path.assert_called_once()


def test_upload_to_gcs_file_not_found(mock_env, mock_gcs, mocker):
    """
    This test simulates a scenario where the local file doesn't exist.
    """
    # Mock os.path.exists to return False
    # simulating that the file to be uploaded doesn't exist.
    mocker.patch('os.path.exists', return_value=False)

    # Capture prints
    mocker.patch('builtins.print')

    # Define the parameter
    path = Path('data/test_file.csv')

    # Call the function
    upload_to_gcs.fn(path)

    # Verify that the print function was called with the 'does not exist' message
    print.assert_called_once_with(f"The file '{path}' does not exist.")


def test_upload_to_gcs_upload_fails(mock_env, mock_os, mock_gcs):
    """
    This test simulates a failure in the GCS upload.
    """
    # Config the mock object mock_gcs to raise an exception when its upload_from_path method is called.
    mock_gcs.upload_from_path.side_effect = Exception("Upload failed")

    # Define the parameter
    path = Path('data/test_file.csv')

    # Attempt to call the function and catch the exception
    with pytest.raises(Exception):
        upload_to_gcs.fn(path)
