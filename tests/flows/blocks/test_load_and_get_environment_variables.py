import os
from io import StringIO
import sys
from tempfile import NamedTemporaryFile
from flows.blocks.make_gcp_blocks import load_and_get_environment_variables


def test_load_and_get_environment_variables_successful_with_param():
    """
    Test if the function successfully loads the environment variables
    and return them as a dictionary
    when a valid .env file is provided.
    """
    # Setup: Create a temporary .env file
    with NamedTemporaryFile(mode='w+', delete=False, suffix=".env") as temp_env_file:
        temp_env_file.write('GOOGLE_APPLICATION_CREDENTIALS="test_credentials"\n')
        temp_env_file.write('CREDS_BLOCK_NAME="test_creds_block"\n')
        temp_env_file.write('DATA_LAKE_BUCKET_NAME="test_bucket"\n')
        temp_env_file.write('BUCKET_BLOCK_NAME="test_bucket_block"\n')
        temp_env_file.flush()

        # Execution: Call the function with the path to the temporary .env file
        result = load_and_get_environment_variables(env_path=temp_env_file.name)

        # Assertion: Verify that the returned dictionary has the values we expect
        assert result == {
            "credentials_file_path": "test_credentials",
            "credentials_block_name": "test_creds_block",
            "bucket_name": "test_bucket",
            "bucket_block_name": "test_bucket_block"
        }

        # Assertion: Verify that the environment variables were loaded correctly
        assert os.getenv('GOOGLE_APPLICATION_CREDENTIALS') == 'test_credentials'
        assert os.getenv('CREDS_BLOCK_NAME') == 'test_creds_block'
        assert os.getenv('DATA_LAKE_BUCKET_NAME') == 'test_bucket'
        assert os.getenv('BUCKET_BLOCK_NAME') == 'test_bucket_block'

        # Teardown: Delete the temporary .env file
        os.unlink(temp_env_file.name)

        # Optionally, delete the loaded environment variables
        del os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        del os.environ['CREDS_BLOCK_NAME']
        del os.environ['DATA_LAKE_BUCKET_NAME']
        del os.environ['BUCKET_BLOCK_NAME']


def test_load_and_get_environment_variables_successful_without_param(assert_env_vars):
    """
    This test reads each key-value pair from the .env file
    and checks that the corresponding environment variable
    has the same value.
    It uses pytest's assert statement to check the conditions.
    """
    # Define the path to the .env file
    basedir = os.path.abspath(os.path.dirname(__file__))
    env_path = os.path.join(basedir, '../../../.env')

    # Execution: Call the function
    result = load_and_get_environment_variables()

    # Assertion: Verify that the env variables match the .env file
    assert_env_vars(env_path)

    # Assertion: Verify that the environment variables were loaded correctly
    assert os.getenv('GOOGLE_APPLICATION_CREDENTIALS') == result["credentials_file_path"]
    assert os.getenv('CREDS_BLOCK_NAME') == result["credentials_block_name"]
    assert os.getenv('DATA_LAKE_BUCKET_NAME') == result["bucket_name"]
    assert os.getenv('BUCKET_BLOCK_NAME') == result["bucket_block_name"]


def test_load_and_get_environment_variables_not_found():
    """
    This test captures the standard output and
    checks that the correct error message is printed
    when an invalid path is provided.
    This aligns with the existing behavior of your load_and_get_environment_variables function.
    """
    # Setup: Provide an invalid path
    invalid_path = "non_existent_path.env"

    # Redirect stdout to capture printed messages
    captured_output = StringIO()
    sys.stdout = captured_output

    # Execution: Call the function load_and_get_environment_variables
    load_and_get_environment_variables(env_path=invalid_path)

    # Restore stdout
    sys.stdout = sys.__stdout__

    print(captured_output.getvalue())

    # Assertion: Check that the correct error message was printed
    assert "Error loading the file with environment variables." in captured_output.getvalue()
