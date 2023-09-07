import pytest
from flows.blocks.make_gcp_blocks import create_gcp_bucket_block
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket


def test_create_gcp_bucket_block_successful(
        mocker):
    """
    Tests the create_gcp_bucket_block function for a successful case.
    """
    # Mock vars
    mock_cred_block_name = "fake_cred_block_name"
    mock_bucket_name = "fake_bucket_name"
    mock_bucket_block_name = "fake_bucket_block_name"

    # Mock the GcpCredentials.load method and return a MagicMock
    mock_gcp_credentials = mocker.MagicMock(spec=GcpCredentials)
    mock_gcp_credentials_load = mocker.patch("prefect_gcp.GcpCredentials.load", return_value=mock_gcp_credentials)

    # Mock the GcsBucket
    mock_gcs_bucket = mocker.MagicMock(spec=GcsBucket)
    mock_gcs_block = mocker.patch("flows.blocks.make_gcp_blocks.GcsBucket", return_value=mock_gcs_bucket)

    # Call the function
    create_gcp_bucket_block(mock_cred_block_name, mock_bucket_name, mock_bucket_block_name)

    # Assertions
    # Ensure GcpCredentials.load was called with the correct arguments
    mock_gcp_credentials_load.assert_called_once_with(mock_cred_block_name)

    # Ensure the GcsBucket block was instantiated with the correct arguments
    mock_gcs_block.assert_called_once_with(
        gcp_credentials=mock_gcp_credentials,
        bucket=mock_bucket_name
    )

    # Ensure the GcsBucket save method was called with the correct arguments
    mock_gcs_bucket.save.assert_called_once_with(
        mock_bucket_block_name,
        overwrite=True
    )


def test_create_gcp_bucket_block_fails_on_load(mocker):
    """
    Tests that create_gcp_bucket_block raises an exception when trying to load the GcpCredentials block.
    """
    # Mock vars
    mock_cred_block_name = "fake_cred_block_name"
    mock_bucket_name = "fake_bucket_name"
    mock_bucket_block_name = "fake_bucket_block_name"

    # Mock the GcpCredentials.load method to raise an Exception
    mock_load = mocker.patch("prefect_gcp.GcpCredentials.load", side_effect=Exception("Failed to load credentials"))

    # Expect the function to raise an exception
    with pytest.raises(Exception):
        create_gcp_bucket_block(mock_cred_block_name, mock_bucket_name, mock_bucket_block_name)

    # Mock the GcsBucket
    mock_gcs_bucket = mocker.MagicMock(spec=GcsBucket)
    mock_gcs_block = mocker.patch("flows.blocks.make_gcp_blocks.GcsBucket", return_value=mock_gcs_bucket)

    # Ensure the GcpCredentials load was called
    mock_load.assert_called()

    # Ensure the GcsBucket block was not instantiated
    mock_gcs_block.assert_not_called()

    # Ensure the GcsBucket save method was not called
    mock_gcs_bucket.save.assert_not_called()
