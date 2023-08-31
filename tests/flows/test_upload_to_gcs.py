import pytest
from flows.ingest import upload_to_gcs


def test_upload_to_gcs_successful(mock_env, mocker, mock_gcs, file_path):
    """
    This test simulates a successful upload to GCS.
    Fixtures will be automatically executed before running a test.
    :param mock_env: fixture to mock environment variable
    :param mock_gcs: fixture to mock the GcsBucket and its load method
    :param file_path: fixture to store the paths of the CSV files used in tests.
    """
    # Mock os.path.exists to return True
    mocker.patch('os.path.exists', return_value=True)
    # Call the function upload_to_gcs with the defined path.
    # Because we've mocked relevant parts of the code,
    # no actual uploading or file manipulation happens.
    upload_to_gcs.fn(file_path["from_path"], file_path["to_path"])

    # Verify the GCS upload method was called
    # Assert that the upload_from_path method of our mock_gcs object
    # was called exactly once, verifying that the upload was attempted.
    mock_gcs.upload_from_path.assert_called_once()


def test_upload_to_gcs_file_not_found(mock_env, mock_gcs, mocker, file_path):
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


def test_upload_to_gcs_upload_fails(mock_env, mocker, mock_gcs, file_path):
    """
    This test simulates a failure in the GCS upload.
    """
    # Mock os.path.exists to return True
    mocker.patch('os.path.exists', return_value=True)
    # Config the mock object mock_gcs to raise an exception when its upload_from_path method is called.
    mock_gcs.upload_from_path.side_effect = Exception("Upload failed")

    # Attempt to call the function and catch the exception
    with pytest.raises(Exception):
        upload_to_gcs.fn(file_path["from_path"], file_path["to_path"])
