import pytest


def test_extraction_agent_handles_missing_file():
    # Arrange
    file_path = 'path/to/nonexistent/file.txt'

    # Act
    with pytest.raises(FileNotFoundError):
        # Function call that should raise the exception
        extraction_agent.process_file(file_path)

    # Assert
    # Additional assertions can go here if needed
