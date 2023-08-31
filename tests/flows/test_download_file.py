import pytest
import requests
from flows.ingest import download_file


def test_download_file_successful(mock_successful_download, url, csv_name):
    """
    This test will simulate a successful file download
    """
    # Get the mocked content from the fixture
    mocked_content = mock_successful_download

    # Call the function
    path = download_file.fn(url, csv_name)

    # Read the file and check the content
    with open(path, 'rb') as file:
        assert file.read() == mocked_content

    # Clean up by removing the downloaded file
    path.unlink()


def test_download_file_invalid_url(mock_failed_download, url, csv_name):
    """
    This test will simulate a failed download
    """
    # Call the function
    path = download_file.fn(url, csv_name)

    # Check that the file was not created
    assert not path.exists()


def test_download_file_connection_timeout(mocker, url, csv_name):
    """
    This test will simulate a timeout error
    """
    # Mock the requests.get to raise a Timeout exception
    mocker.patch.object(requests, "get", side_effect=requests.exceptions.Timeout)

    # Attempt to call the function with mock data and catch the exception
    with pytest.raises(requests.exceptions.Timeout):
        download_file.fn(url, csv_name)
