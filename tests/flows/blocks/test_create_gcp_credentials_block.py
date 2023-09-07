import pytest
import json
from flows.blocks.make_gcp_blocks import create_gcp_credentials_block
from prefect_gcp import GcpCredentials


def test_create_gcp_credentials_block_successful(
        mocker):
    """
    Tests the create_gcp_credentials_block function by mocking the file read,
    JSON parsing, and GcpCredentials instantiation. It checks if all the
    internal calls are made with the expected arguments and in the expected sequence.
    """
    # Mock the credentials file content
    mock_file_content = '{"key": "value"}'
    mock_cred_file_path = "fake_cred_file_path"
    mock_cred_block_name = "fake_cred_block_name"

    # Mock builtins.open
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_file_content)))

    # Mock json.load to return the valid mock service account information
    mocker.patch('json.load', return_value=mock_file_content)

    # Mock the GcpCredentials
    mock_gcp_credentials = mocker.MagicMock(spec=GcpCredentials)
    mock_cred_block = mocker.patch("flows.blocks.make_gcp_blocks.GcpCredentials", return_value=mock_gcp_credentials)

    # Call the function
    create_gcp_credentials_block(mock_cred_file_path, mock_cred_block_name)

    # Assertions
    # Ensure open was called with the correct path
    open.assert_called_with(mock_cred_file_path, "r")

    # Ensure json.load was called
    json.load.assert_called_once()

    # Ensure the GcpCredentials block was instantiated with the correct arguments
    mock_cred_block.assert_called_once_with(
        service_account_info=mock_file_content
    )

    # Ensure the GcpCredentials save method was called with the correct arguments
    mock_gcp_credentials.save.assert_called_once_with(
        mock_cred_block_name,
        overwrite=True
    )


def test_create_gcp_credentials_block_fails_on_bad_json(
        mocker):
    """
    Tests that create_gcp_credentials_block raises an exception when it encounters a malformed JSON file.
    """
    # Mock the credentials file content
    mock_cred_file_path = "fake_path"
    mock_cred_block_name = "fake_block_name"
    # Mock builtins.open
    mocker.patch('builtins.open', mocker.mock_open(read_data="Not a JSON"))

    # Mock json.load to raise a JSONDecodeError
    mocker.patch('json.load', side_effect=json.JSONDecodeError("Bad JSON", doc="Not a JSON", pos=0))

    # Mock the GcpCredentials
    mock_gcp_credentials = mocker.MagicMock(spec=GcpCredentials)
    mock_cred_block = mocker.patch("flows.blocks.make_gcp_blocks.GcpCredentials", return_value=mock_gcp_credentials)

    # Expect a JSONDecodeError to be raised when calling the function
    with pytest.raises(json.JSONDecodeError):
        create_gcp_credentials_block(mock_cred_file_path, mock_cred_block_name)

    # Assertions
    # Ensure open was called with the correct path
    open.assert_called_with(mock_cred_file_path, "r")

    # Ensure json.load was called
    json.load.assert_called_once()

    # Ensure the GcpCredentials block was not instantiated
    mock_cred_block.assert_not_called()

    # Ensure the GcpCredentials save method was not called
    mock_gcp_credentials.save.assert_not_called()
