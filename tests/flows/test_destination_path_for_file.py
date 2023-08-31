from pathlib import Path
from flows.ingest import destination_path_for_file


def test_destination_path_for_file_single_folder():
    """
    Test case for a file located in a single folder.
    """
    original_path = Path("data/city/file.csv")
    expected_path = Path("data/raw/city/file.csv")
    assert destination_path_for_file(original_path) == expected_path


def test_destination_path_for_file_nested_folders():
    """
    Test case for a file located in nested folders.
    """
    original_path = Path("data/city/subfolder/file.csv")
    expected_path = Path("data/raw/city/subfolder/file.csv")
    assert destination_path_for_file(original_path) == expected_path


def test_destination_path_for_file_root_folder():
    """
    Test case for a file located in the root folder.
    """
    original_path = Path("file.csv")
    expected_path = Path("raw/file.csv")
    assert destination_path_for_file(original_path) == expected_path


def test_destination_path_for_file_empty_path():
    """
    Test case for an empty path.
    """
    original_path = Path("")
    expected_path = Path("raw/")
    assert destination_path_for_file(original_path) == expected_path
