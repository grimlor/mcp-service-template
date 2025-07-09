"""
Test suite for File Processing Domain

This module contains unit tests for file processing tools.
"""

import csv
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Note: These tests use the template placeholders and will work after setup_template.py is run


class TestFileProcessingTools:
    """Test file processing domain functionality."""

    @pytest.fixture
    def temp_csv_file(self):
        """Create a temporary CSV file for testing."""
        data = [
            ["name", "age", "city"],
            ["John Doe", "30", "New York"],
            ["Jane Smith", "25", "Los Angeles"],
            ["Bob Johnson", "35", "Chicago"],
        ]

        fd, path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)

        yield path
        os.unlink(path)

    @pytest.fixture
    def temp_json_file(self):
        """Create a temporary JSON file for testing."""
        data = {
            "users": [
                {"id": 1, "name": "John Doe", "email": "john@example.com"},
                {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
            ],
            "metadata": {"total": 2, "version": "1.0"},
        }

        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)

        yield path
        os.unlink(path)

    @pytest.fixture
    def temp_text_file(self):
        """Create a temporary text file for testing."""
        content = """This is a sample text file.
It contains multiple lines.
Each line has different content.
Some lines are longer than others, with more detailed information.
This is the last line."""

        fd, path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w") as f:
            f.write(content)

        yield path
        os.unlink(path)

    def test_file_processing_tools_import(self):
        """Test that file processing tools can be imported."""
        try:
            from service_name_mcp.file_processing_domain import file_processing_tools

            assert file_processing_tools is not None
        except ImportError as e:
            pytest.fail(f"Failed to import file processing tools: {e}")

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_read_csv_file(self, mock_logger, temp_csv_file):
        """Test CSV file reading."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_csv_file

        result = read_csv_file(file_path=temp_csv_file)

        assert isinstance(result, list)
        assert len(result) > 0
        # Check header
        assert result[0] == ["name", "age", "city"]
        # Check data rows
        assert len(result) == 4  # header + 3 data rows
        assert "John Doe" in result[1]
        mock_logger.info.assert_called()

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_read_csv_with_limit(self, mock_logger, temp_csv_file):
        """Test CSV file reading with row limit."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_csv_file

        result = read_csv_file(file_path=temp_csv_file, max_rows=2)

        assert isinstance(result, list)
        assert len(result) <= 2
        mock_logger.info.assert_called()

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_read_json_file(self, mock_logger, temp_json_file):
        """Test JSON file reading."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_json_file

        result = read_json_file(file_path=temp_json_file)

        assert isinstance(result, dict)
        assert "users" in result
        assert "metadata" in result
        assert len(result["users"]) == 2
        assert result["metadata"]["total"] == 2
        mock_logger.info.assert_called()

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_read_text_file(self, mock_logger, temp_text_file):
        """Test text file reading."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_text_file

        result = read_text_file(file_path=temp_text_file)

        assert isinstance(result, str)
        assert "sample text file" in result
        assert len(result.split("\n")) == 5  # 5 lines
        mock_logger.info.assert_called()

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_read_text_file_with_limit(self, mock_logger, temp_text_file):
        """Test text file reading with line limit."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_text_file

        result = read_text_file(file_path=temp_text_file, max_lines=3)

        assert isinstance(result, str)
        lines = result.split("\n")
        assert len(lines) <= 3
        mock_logger.info.assert_called()

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_analyze_csv_structure(self, mock_logger, temp_csv_file):
        """Test CSV structure analysis."""
        from service_name_mcp.file_processing_domain.file_processing_tools import analyze_csv_structure

        result = analyze_csv_structure(file_path=temp_csv_file)

        assert isinstance(result, dict)
        assert "columns" in result
        assert "row_count" in result
        assert "sample_data" in result
        assert result["columns"] == ["name", "age", "city"]
        assert result["row_count"] == 3  # Data rows, not including header
        mock_logger.info.assert_called()

    def test_file_path_validation(self):
        """Test file path validation."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_text_file

        # Test with non-existent file
        with pytest.raises(Exception):  # noqa: B017
            read_text_file(file_path="/nonexistent/file.txt")

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_write_csv_file(self, mock_logger):
        """Test CSV file writing."""
        from service_name_mcp.file_processing_domain.file_processing_tools import write_csv_file

        data = [["name", "score"], ["Alice", "95"], ["Bob", "87"]]

        fd, temp_path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)

        try:
            result = write_csv_file(file_path=temp_path, data=data)

            assert result is True or "success" in str(result).lower()

            # Verify file was written correctly
            with open(temp_path) as f:
                reader = csv.reader(f)
                written_data = list(reader)
                assert written_data == data

            mock_logger.info.assert_called()
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_write_json_file(self, mock_logger):
        """Test JSON file writing."""
        from service_name_mcp.file_processing_domain.file_processing_tools import write_json_file

        data = {"test": "data", "numbers": [1, 2, 3], "nested": {"key": "value"}}

        fd, temp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)

        try:
            result = write_json_file(file_path=temp_path, data=data)

            assert result is True or "success" in str(result).lower()

            # Verify file was written correctly
            with open(temp_path) as f:
                written_data = json.load(f)
                assert written_data == data

            mock_logger.info.assert_called()
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestFileOperations:
    """Test file system operations."""

    @pytest.fixture
    def temp_directory(self):
        """Create a temporary directory with test files."""
        import shutil
        import tempfile

        temp_dir = tempfile.mkdtemp()

        # Create test files
        (Path(temp_dir) / "file1.txt").write_text("Content 1")
        (Path(temp_dir) / "file2.csv").write_text("col1,col2\nval1,val2")
        (Path(temp_dir) / "file3.json").write_text('{"key": "value"}')

        # Create subdirectory
        sub_dir = Path(temp_dir) / "subdir"
        sub_dir.mkdir()
        (sub_dir / "nested.txt").write_text("Nested content")

        yield temp_dir
        shutil.rmtree(temp_dir)

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_list_files_in_directory(self, mock_logger, temp_directory):
        """Test directory file listing."""
        from service_name_mcp.file_processing_domain.file_processing_tools import list_files_in_directory

        result = list_files_in_directory(directory_path=temp_directory)

        assert isinstance(result, list)
        assert len(result) >= 3  # At least our test files

        # Check that file extensions are included
        file_names = [item["name"] if isinstance(item, dict) else item for item in result]
        assert any("txt" in name for name in file_names)
        assert any("csv" in name for name in file_names)
        assert any("json" in name for name in file_names)

        mock_logger.info.assert_called()

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_list_files_with_filter(self, mock_logger, temp_directory):
        """Test directory file listing with extension filter."""
        from service_name_mcp.file_processing_domain.file_processing_tools import list_files_in_directory

        result = list_files_in_directory(directory_path=temp_directory, file_extension_filter=".txt")

        assert isinstance(result, list)
        # Should only include .txt files
        for item in result:
            file_name = item["name"] if isinstance(item, dict) else item
            assert file_name.endswith(".txt")

        mock_logger.info.assert_called()


class TestDataTransformation:
    """Test data transformation functions."""

    def test_csv_to_dict_conversion(self):
        """Test converting CSV data to dictionary format."""
        from service_name_mcp.file_processing_domain.file_processing_tools import csv_to_dict

        csv_data = [["name", "age", "city"], ["John", "30", "NYC"], ["Jane", "25", "LA"]]

        result = csv_to_dict(csv_data)

        assert isinstance(result, list)
        assert len(result) == 2  # Two data rows
        assert result[0]["name"] == "John"
        assert result[0]["age"] == "30"
        assert result[1]["name"] == "Jane"

    def test_filter_data(self):
        """Test data filtering functionality."""
        from service_name_mcp.file_processing_domain.file_processing_tools import filter_data

        data = [
            {"name": "John", "age": 30, "city": "NYC"},
            {"name": "Jane", "age": 25, "city": "LA"},
            {"name": "Bob", "age": 35, "city": "NYC"},
        ]

        # Filter by city
        result = filter_data(data, criteria={"city": "NYC"})

        assert isinstance(result, list)
        assert len(result) == 2  # John and Bob
        assert all(item["city"] == "NYC" for item in result)


class TestBestPractices:
    """Test file processing best practices and documentation."""

    def test_best_practices_file_exists(self):
        """Test that best practices documentation exists."""
        from pathlib import Path

        # Get the path to the best practices file
        current_dir = Path(__file__).parent.parent.parent
        best_practices_path = current_dir / "src" / "service_name_mcp" / "file_processing_domain" / "best_practices.md"

        assert best_practices_path.exists(), "File processing best practices file should exist"

        # Verify it has content
        content = best_practices_path.read_text()
        assert len(content) > 100, "Best practices should have substantial content"
        assert any(
            keyword in content.lower() for keyword in ["file", "csv", "json"]
        ), "Best practices should mention file processing concepts"


# Integration tests
class TestFileProcessingIntegration:
    """Integration tests for file processing domain."""

    def test_mcp_tool_registration(self):
        """Test that file processing tools are properly registered with MCP."""
        try:
            # Import the tools module to trigger registration
            from service_name_mcp.mcp_instance import mcp

            # This test verifies that import doesn't fail
            assert mcp is not None

        except ImportError as e:
            pytest.fail(f"Failed to register file processing tools with MCP: {e}")

    @pytest.mark.integration
    def test_end_to_end_file_workflow(self, temp_csv_file, temp_json_file):
        """Test complete file processing workflow."""
        from service_name_mcp.file_processing_domain.file_processing_tools import (
            analyze_csv_structure,
            read_csv_file,
            read_json_file,
        )

        # 1. Read and analyze CSV
        csv_data = read_csv_file(temp_csv_file)
        assert len(csv_data) > 0

        csv_structure = analyze_csv_structure(temp_csv_file)
        assert "columns" in csv_structure
        assert "row_count" in csv_structure

        # 2. Read JSON for comparison
        json_data = read_json_file(temp_json_file)
        assert isinstance(json_data, dict)

        # 3. Verify data integrity
        assert len(csv_data) == csv_structure["row_count"] + 1  # +1 for header


if __name__ == "__main__":
    pytest.main([__file__])
