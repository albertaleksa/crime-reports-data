import pytest
import requests
from flows.ingest import download_file


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
def mock_timeout_download(mock_requests_get):
    """
    This fixture simulates a timeout error
    by making the mocked request raise a Timeout exception.
    """
    mock_requests_get.side_effect = requests.exceptions.Timeout


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
