from io import StringIO
import sys
import os
from tempfile import NamedTemporaryFile
from flows.ingest import load_env


def test_load_env_successful_with_param():
    """
    Test if the function successfully loads the environment variables
    when a valid .env file is provided.
    """
    # Setup: Create a temporary .env file
    with NamedTemporaryFile(mode='w+', delete=False, suffix=".env") as temp_env_file:
        temp_env_file.write('PROJECT_ID="test_project"\n')
        temp_env_file.write('REGION="test_region"\n')
        temp_env_file.flush()
        # Add other test values as needed

        # Execution: Call the underlying function of the load_env task
        """
        By calling load_env.fn(), you are invoking the actual function wrapped by the task,
        bypassing the Prefect task execution logic.
        This allows you to test the function's behavior directly,
        without needing to be inside a Prefect flow context.
        """
        # Call the load_env function with the path to the temporary .env file
        load_env.fn(env_path=temp_env_file.name)  # Call the underlying function instead of the task object

        # Assertion: Verify that the environment variables were loaded correctly
        assert os.getenv('PROJECT_ID') == 'test_project'
        assert os.getenv('REGION') == 'test_region'
        # Add other assertions as needed

        # Teardown: Delete the temporary .env file
        os.unlink(temp_env_file.name)

        # Optionally, delete the loaded environment variables
        del os.environ['PROJECT_ID']
        del os.environ['REGION']


def test_load_env_successful_without_param():
    """
    This test reads each key-value pair from the .env file
    and checks that the corresponding environment variable
    has the same value.
    It uses pytest's assert statement to check the conditions.
    """
    # Define the path to the .env file
    basedir = os.path.abspath(os.path.dirname(__file__))
    env_path = os.path.join(basedir, '../../.env')

    # Execution: Call the underlying function of the load_env task
    load_env.fn()

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


def test_load_env_file_not_found():
    """
    This test captures the standard output and
    checks that the correct error message is printed
    when an invalid path is provided.
    This aligns with the existing behavior of your load_env function.
    """
    # Setup: Provide an invalid path
    invalid_path = "non_existent_path.env"

    # Redirect stdout to capture printed messages
    captured_output = StringIO()
    sys.stdout = captured_output

    # Execution: Call the underlying function of the load_env task
    load_env.fn(env_path=invalid_path)

    # Restore stdout
    sys.stdout = sys.__stdout__

    print(captured_output.getvalue())

    # Assertion: Check that the correct error message was printed
    assert "Error loading the file with environment variables." in captured_output.getvalue()

