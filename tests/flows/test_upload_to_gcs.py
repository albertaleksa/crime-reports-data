import pytest
from flows.ingest import upload_to_gcs
from prefect_gcp.cloud_storage import GcsBucket


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


def test_upload_to_gcs_successful(mock_env,
                                  mocker,
                                  mock_gcs_bucket,
                                  mock_gcs_bucket_load,
                                  file_path):
    """
    This test simulates a successful upload to GCS.
    Fixtures will be automatically executed before running a test.
    :param mock_env: fixture to mock environment variable
    :param mock_gcs_bucket: fixture to mock the GcsBucket
    :param mock_gcs_bucket_load: fixture to mock the GcsBucket load method
    :param file_path: fixture to store the paths of the CSV files used in tests.
    """
    # Mock os.path.exists to return True
    mocker.patch('os.path.exists', return_value=True)

    # Call the function upload_to_gcs with the defined path.
    # Because we've mocked relevant parts of the code,
    # no actual uploading or file manipulation happens.
    upload_to_gcs.fn(file_path["from_path"], file_path["to_path"])

    # Assertions
    # Ensure GcsBucket.load was called with the correct arguments
    mock_gcs_bucket_load.assert_called_once()

    # Verify the GCS upload method was called
    # Assert that the upload_from_path method of our mock_gcs object
    # was called exactly once, verifying that the upload was attempted.
    mock_gcs_bucket.upload_from_path.assert_called_once_with(
        from_path=f"{file_path['from_path']}",
        to_path=f"{file_path['to_path']}",
        timeout=300
    )


def test_upload_to_gcs_file_not_found(mock_env,
                                      mocker,
                                      mock_gcs_bucket,
                                      mock_gcs_bucket_load,
                                      file_path):
    """
    This test simulates a scenario where the local file doesn't exist.
    """
    # Mock os.path.exists to return False
    # simulating that the file to be uploaded doesn't exist.
    mocker.patch('os.path.exists', return_value=False)

    # Capture prints
    mocker.patch('builtins.print')

    # Call the function
    upload_to_gcs.fn(file_path["from_path"], file_path["to_path"])
    from_path = file_path["from_path"]

    # Verify that the print function was called with the 'does not exist' message
    print.assert_called_once_with(f"The file '{from_path}' does not exist.")

    # Ensure the GcsBucket load was called
    mock_gcs_bucket_load.assert_called()

    # Ensure the GcsBucket upload_from_path method was not called
    mock_gcs_bucket.upload_from_path.assert_not_called()


def test_upload_to_gcs_upload_fails(mock_env,
                                    mocker,
                                    mock_gcs_bucket,
                                    mock_gcs_bucket_load,
                                    file_path):
    """
    This test simulates a failure in the GCS upload.
    """
    # Mock os.path.exists to return True
    mocker.patch('os.path.exists', return_value=True)

    # Config the mock object mock_gcs to raise an exception when its upload_from_path method is called.
    mock_gcs_bucket.upload_from_path.side_effect = Exception("Upload failed")

    # Attempt to call the function and catch the exception
    with pytest.raises(Exception):
        upload_to_gcs.fn(file_path["from_path"], file_path["to_path"])

    # Ensure the GcsBucket load was called
    mock_gcs_bucket_load.assert_called()

    # Ensure the GcsBucket upload_from_path method was called
    mock_gcs_bucket.upload_from_path.assert_called_once()
