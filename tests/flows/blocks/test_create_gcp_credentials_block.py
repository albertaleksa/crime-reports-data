import pytest
import json
from flows.blocks.make_gcp_blocks import create_gcp_credentials_block


def test_create_gcp_credentials_block_successful(mock_gcp_creds_in_make_gcp_blocks, mocker):
    """
    Tests the create_gcp_credentials_block function by mocking the file read,
    JSON parsing, and GcpCredentials instantiation. It checks if all the
    internal calls are made with the expected arguments and in the expected sequence.
    """
    # Mock the credentials file content
    mock_file_content = '{"key": "value"}'

    # Mock builtins.open
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_file_content)))

    # Mock json.load to return the valid mock service account information
    mocker.patch('json.load', return_value=mock_file_content)

    # Call the function
    create_gcp_credentials_block("fake_path", "fake_block_name")

    # Assertions
    # Ensure open was called with the correct path
    open.assert_called_with("fake_path", "r")

    # Ensure json.load was called
    json.load.assert_called_once()

    # Ensure the GcpCredentials save method was called with the correct arguments
    mock_gcp_creds_in_make_gcp_blocks.save.assert_called_once_with("fake_block_name", overwrite=True)


def test_create_gcp_credentials_block_fails_on_bad_json(mock_gcp_creds_in_make_gcp_blocks, mocker):
    """
    Tests that create_gcp_credentials_block raises an exception when it encounters a malformed JSON file.
    """
    # Mock builtins.open
    mocker.patch('builtins.open', mocker.mock_open(read_data="Not a JSON"))

    # Mock json.load to raise a JSONDecodeError
    mocker.patch('json.load', side_effect=json.JSONDecodeError("Bad JSON", doc="Not a JSON", pos=0))

    # Expect a JSONDecodeError to be raised when calling the function
    with pytest.raises(json.JSONDecodeError):
        create_gcp_credentials_block("fake_path", "fake_block_name")

    # Assertions
    # Ensure open was called with the correct path
    open.assert_called_with("fake_path", "r")

    # Ensure json.load was called
    json.load.assert_called_once()

    # Ensure the GcpCredentials save method was not called
    mock_gcp_creds_in_make_gcp_blocks.save.assert_not_called()
