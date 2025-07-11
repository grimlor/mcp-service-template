"""
Test suite for File Processing Domain - Working Functions

This module contains unit tests for the actually implemented file processing functions.
"""

import csv
import json
import os
import tempfile
from unittest.mock import patch

import pytest


class TestFileProcessingWorkingTools:
    """Test file processing domain functionality - working functions only."""

    @pytest.fixture
    def temp_csv_file(self):
        """Create a temporary CSV file for testing."""
        fd, path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "age", "city"])
            writer.writerow(["Alice", "30", "New York"])
            writer.writerow(["Bob", "25", "Los Angeles"])
            writer.writerow(["Carol", "35", "Chicago"])
        yield path
        os.unlink(path)

    @pytest.fixture
    def temp_json_file(self):
        """Create a temporary JSON file for testing."""
        fd, path = tempfile.mkstemp(suffix=".json")
        data = {
            "metadata": {"total": 2, "version": "1.0"},
            "users": [{"id": 1, "name": "Alice Smith"}, {"id": 2, "name": "Jane Smith"}],
        }
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        yield path
        os.unlink(path)

    @pytest.fixture
    def temp_text_file(self):
        """Create a temporary text file for testing."""
        fd, path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w") as f:
            f.write("Line 1: Hello world\n")
            f.write("Line 2: This is a test\n")
            f.write("Line 3: Python testing\n")
            f.write("Line 4: File processing\n")
        yield path
        os.unlink(path)

    @pytest.fixture
    def temp_directory(self):
        """Create a temporary directory with files for testing."""
        temp_dir = tempfile.mkdtemp()

        # Create test files
        with open(os.path.join(temp_dir, "test1.csv"), "w") as f:
            f.write("col1,col2\\nval1,val2\\n")

        with open(os.path.join(temp_dir, "test2.json"), "w") as f:
            json.dump({"test": "data"}, f)

        with open(os.path.join(temp_dir, "test3.txt"), "w") as f:
            f.write("Test content")

        yield temp_dir

        # Cleanup
        import shutil

        shutil.rmtree(temp_dir)

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_read_csv_file_success(self, mock_logger, temp_csv_file):
        """Test successful CSV file reading."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_csv_file

        result = read_csv_file(file_path=temp_csv_file)

        assert isinstance(result, dict)
        assert "data" in result
        assert "structure" in result
        assert "column_analysis" in result
        assert result["structure"]["total_rows_read"] == 3
        assert result["structure"]["column_count"] == 3

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_read_csv_file_with_limit(self, mock_logger, temp_csv_file):
        """Test CSV file reading with row limit."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_csv_file

        result = read_csv_file(file_path=temp_csv_file, max_rows=2)

        assert isinstance(result, dict)
        assert "data" in result
        assert result["structure"]["total_rows_read"] <= 2

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_read_csv_file_not_found(self, mock_logger):
        """Test CSV file reading with non-existent file."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_csv_file

        result = read_csv_file(file_path="/nonexistent/file.csv")

        assert isinstance(result, dict)
        assert "error" in result
        assert "File not found" in result["error"]

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_read_json_file_success(self, mock_logger, temp_json_file):
        """Test successful JSON file reading."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_json_file

        result = read_json_file(file_path=temp_json_file)

        assert isinstance(result, dict)
        assert "data" in result
        assert "analysis" in result
        assert "file_info" in result

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_read_json_file_not_found(self, mock_logger):
        """Test JSON file reading with non-existent file."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_json_file

        result = read_json_file(file_path="/nonexistent/file.json")

        assert isinstance(result, dict)
        assert "error" in result
        assert "File not found" in result["error"]

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_analyze_text_file_success(self, mock_logger, temp_text_file):
        """Test successful text file analysis."""
        from service_name_mcp.file_processing_domain.file_processing_tools import analyze_text_file

        result = analyze_text_file(file_path=temp_text_file)

        assert isinstance(result, dict)
        assert "statistics" in result
        assert "content_analysis" in result
        assert "file_info" in result
        assert result["statistics"]["total_lines"] == 4

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_analyze_text_file_with_limit(self, mock_logger, temp_text_file):
        """Test text file analysis with line limit."""
        from service_name_mcp.file_processing_domain.file_processing_tools import analyze_text_file

        result = analyze_text_file(file_path=temp_text_file, max_lines=2)

        assert isinstance(result, dict)
        assert "statistics" in result
        assert result["statistics"]["total_lines"] <= 2

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_analyze_text_file_not_found(self, mock_logger):
        """Test text file analysis with non-existent file."""
        from service_name_mcp.file_processing_domain.file_processing_tools import analyze_text_file

        result = analyze_text_file(file_path="/nonexistent/file.txt")

        assert isinstance(result, dict)
        assert "error" in result
        assert "File not found" in result["error"]

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_write_csv_file_success(self, mock_logger):
        """Test successful CSV file writing."""
        from service_name_mcp.file_processing_domain.file_processing_tools import write_csv_file

        data = [{"name": "Alice", "score": "95"}, {"name": "Bob", "score": "87"}]

        fd, temp_path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)

        try:
            result = write_csv_file(file_path=temp_path, data=data)

            assert isinstance(result, dict)
            assert result["status"] == "success"
            assert result["rows_written"] == 2
            assert os.path.exists(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_write_csv_file_empty_data(self, mock_logger):
        """Test CSV file writing with empty data."""
        from service_name_mcp.file_processing_domain.file_processing_tools import write_csv_file

        result = write_csv_file(file_path="/tmp/test.csv", data=[])

        assert isinstance(result, dict)
        assert "error" in result
        assert "No data provided" in result["error"]

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_write_json_file_success(self, mock_logger):
        """Test successful JSON file writing."""
        from service_name_mcp.file_processing_domain.file_processing_tools import write_json_file

        data = {"users": [{"id": 1, "name": "Alice"}], "total": 1}

        fd, temp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)

        try:
            result = write_json_file(file_path=temp_path, data=data)

            assert isinstance(result, dict)
            assert result["status"] == "success"
            assert os.path.exists(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_list_directory_files_success(self, mock_logger, temp_directory):
        """Test successful directory file listing."""
        from service_name_mcp.file_processing_domain.file_processing_tools import list_directory_files

        result = list_directory_files(directory_path=temp_directory)

        assert isinstance(result, dict)
        assert "files" in result
        assert "summary" in result
        assert result["summary"]["total_files"] == 3

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_list_directory_files_with_filter(self, mock_logger, temp_directory):
        """Test directory file listing with file type filter."""
        from service_name_mcp.file_processing_domain.file_processing_tools import list_directory_files

        result = list_directory_files(directory_path=temp_directory, file_types=[".csv"])

        assert isinstance(result, dict)
        assert "files" in result
        assert result["summary"]["total_files"] == 1
        assert all(f["extension"] == ".csv" for f in result["files"])

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_list_directory_files_not_found(self, mock_logger):
        """Test directory listing with non-existent directory."""
        from service_name_mcp.file_processing_domain.file_processing_tools import list_directory_files

        result = list_directory_files(directory_path="/nonexistent/directory")

        assert isinstance(result, dict)
        assert "error" in result
        assert "Directory not found" in result["error"]

    @patch("service_name_mcp.file_processing_domain.file_processing_tools.logger")
    def test_create_sample_files_success(self, mock_logger):
        """Test successful sample file creation."""
        from service_name_mcp.file_processing_domain.file_processing_tools import create_sample_files

        temp_dir = tempfile.mkdtemp()

        try:
            result = create_sample_files(output_directory=temp_dir)

            assert isinstance(result, dict)
            assert result["status"] == "success"
            assert result["total_files"] >= 4  # Should create multiple sample files
            assert os.path.exists(temp_dir)

            # Check that files were actually created
            files_created = [f["file"] for f in result["files_created"]]
            assert "customers.csv" in files_created
            assert "product_catalog.json" in files_created
        finally:
            import shutil

            shutil.rmtree(temp_dir)

    def test_analyze_csv_columns_function(self):
        """Test CSV column analysis helper function."""
        from service_name_mcp.file_processing_domain.file_processing_tools import analyze_csv_columns

        data = [
            {"name": "Alice", "age": "30", "score": "95.5"},
            {"name": "Bob", "age": "25", "score": "87.2"},
            {"name": "Carol", "age": "35", "score": "92.8"},
        ]
        headers = ["name", "age", "score"]

        result = analyze_csv_columns(data, headers)

        assert isinstance(result, dict)
        assert "name" in result
        assert "age" in result
        assert "score" in result
        assert result["age"]["likely_numeric"] is True
        assert result["score"]["likely_numeric"] is True

    def test_analyze_json_structure_function(self):
        """Test JSON structure analysis helper function."""
        from service_name_mcp.file_processing_domain.file_processing_tools import analyze_json_structure

        data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}], "metadata": {"total": 2}}

        result = analyze_json_structure(data)

        assert isinstance(result, dict)
        assert "type" in result
        assert "structure" in result
        assert "size_estimate" in result


class TestFileProcessingIntegration:
    """Integration tests for file processing workflow."""

    @pytest.mark.integration
    def test_full_workflow_csv_processing(self):
        """Test complete CSV processing workflow."""
        from service_name_mcp.file_processing_domain.file_processing_tools import (
            list_directory_files,
            read_csv_file,
            write_csv_file,
        )

        temp_dir = tempfile.mkdtemp()

        try:
            # 1. Write CSV file
            data = [
                {"product": "Laptop", "price": "999.99", "category": "Electronics"},
                {"product": "Chair", "price": "199.99", "category": "Furniture"},
            ]

            csv_path = os.path.join(temp_dir, "products.csv")
            write_result = write_csv_file(file_path=csv_path, data=data)
            assert write_result["status"] == "success"

            # 2. Read CSV file back
            read_result = read_csv_file(file_path=csv_path)
            assert "data" in read_result
            assert len(read_result["data"]) == 2

            # 3. List files in directory
            list_result = list_directory_files(directory_path=temp_dir, file_types=[".csv"])
            assert list_result["summary"]["total_files"] == 1

        finally:
            import shutil

            shutil.rmtree(temp_dir)

    @pytest.mark.integration
    def test_full_workflow_json_processing(self):
        """Test complete JSON processing workflow."""
        from service_name_mcp.file_processing_domain.file_processing_tools import read_json_file, write_json_file

        temp_dir = tempfile.mkdtemp()

        try:
            # 1. Write JSON file
            data = {
                "catalog": {"products": [{"id": 1, "name": "Product A"}, {"id": 2, "name": "Product B"}]},
                "metadata": {"version": "1.0", "total": 2},
            }

            json_path = os.path.join(temp_dir, "catalog.json")
            write_result = write_json_file(file_path=json_path, data=data)
            assert write_result["status"] == "success"

            # 2. Read JSON file back
            read_result = read_json_file(file_path=json_path)
            assert "data" in read_result
            assert read_result["data"]["metadata"]["total"] == 2

        finally:
            import shutil

            shutil.rmtree(temp_dir)
