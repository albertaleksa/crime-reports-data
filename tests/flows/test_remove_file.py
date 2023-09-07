from pathlib import Path
from flows.ingest import remove_file


def test_remove_file_exists(mocker):
    """
    Test case for a file that exists.
    """
    # Mock os.path.exists to return True
    mocker.patch('os.path.exists', return_value=True)

    # Mock os.remove so that it does not actually remove any files
    mocker.patch('os.remove')

    # Mock print to capture output
    mock_print = mocker.patch('builtins.print')

    # Define the parameter
    path = Path('data/test_file.csv')

    # Call the function
    remove_file(path)

    # Verify that the print function was called with the 'was removed' message
    mock_print.assert_called_once_with(f"The file {path} was removed.")


def test_remove_file_does_not_exist(mocker):
    """
    Test case for a file that does not exist.
    """
    # Mock os.path.exists to return False
    mocker.patch('os.path.exists', return_value=False)

    # Mock print to capture output
    mock_print = mocker.patch('builtins.print')

    # Define the parameter
    path = Path('data/test_file.csv')

    # Call the function
    remove_file(path)

    # Verify that the print function was called with the 'does not exist' message
    mock_print.assert_called_once_with(f"The file '{path}' does not exist.")
