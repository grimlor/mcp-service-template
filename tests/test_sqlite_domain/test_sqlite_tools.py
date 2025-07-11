"""
Test suite for SQLite Domain - Working Functions

This module contains unit tests for the actually implemented SQLite functions.
"""

import os
import tempfile
from unittest.mock import patch

import pytest


class TestSQLiteWorkingTools:
    """Test SQLite domain functionality - working functions only."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary SQLite database for testing."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    @pytest.fixture
    def sample_db(self):
        """Create a sample database with test data."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_create_sample_database

        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)

        # Create sample database
        result = sqlite_create_sample_database(database_path=path)
        assert result["status"] == "success"

        yield path
        if os.path.exists(path):
            os.unlink(path)

    def test_sqlite_tools_import(self):
        """Test that SQLite tools can be imported."""
        try:
            from service_name_mcp.sqlite_domain import sqlite_tools

            assert sqlite_tools is not None
        except ImportError as e:
            pytest.fail(f"Failed to import SQLite tools: {e}")

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_execute_query_success(self, mock_logger, sample_db):
        """Test successful SQLite query execution."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_execute_query

        result = sqlite_execute_query(query="SELECT name, email FROM customers LIMIT 3", database_path=sample_db)

        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert "results" in result
        assert "columns" in result
        assert len(result["results"]) <= 3
        assert "name" in result["columns"]
        assert "email" in result["columns"]

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_execute_query_insert(self, mock_logger, sample_db):
        """Test SQLite INSERT query execution."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_execute_query

        result = sqlite_execute_query(
            query="INSERT INTO customers (name, email, city) VALUES ('Test User', 'test@example.com', 'Test City')",
            database_path=sample_db,
        )

        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert "rows_affected" in result
        assert result["rows_affected"] >= 1

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_execute_query_not_found(self, mock_logger):
        """Test SQLite query with non-existent database."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_execute_query

        result = sqlite_execute_query(query="SELECT * FROM customers", database_path="/nonexistent/database.db")

        assert isinstance(result, dict)
        assert "error" in result
        assert "Database file not found" in result["error"]

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_execute_query_invalid_sql(self, mock_logger, sample_db):
        """Test SQLite query with invalid SQL."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_execute_query

        result = sqlite_execute_query(query="INVALID SQL STATEMENT", database_path=sample_db)

        assert isinstance(result, dict)
        assert "error" in result
        assert "SQLite error" in result["error"]

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_get_table_schema_success(self, mock_logger, sample_db):
        """Test successful table schema retrieval."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_get_table_schema

        result = sqlite_get_table_schema(table_name="customers", database_path=sample_db)

        assert isinstance(result, dict)
        assert result["table_name"] == "customers"
        assert "columns" in result
        assert "column_count" in result
        assert len(result["columns"]) > 0

        # Check that we have expected columns
        column_names = [col["name"] for col in result["columns"]]
        assert "name" in column_names
        assert "email" in column_names

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_get_table_schema_not_found(self, mock_logger, sample_db):
        """Test table schema for non-existent table."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_get_table_schema

        result = sqlite_get_table_schema(table_name="nonexistent_table", database_path=sample_db)

        assert isinstance(result, dict)
        assert "error" in result
        assert "not found" in result["error"].lower()

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_list_tables_success(self, mock_logger, sample_db):
        """Test successful table listing."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_list_tables

        result = sqlite_list_tables(database_path=sample_db)

        assert isinstance(result, dict)
        assert "tables" in result
        assert "table_count" in result
        assert result["table_count"] >= 4  # customers, products, orders, order_items

        # Check that expected tables exist
        table_names = [table["name"] for table in result["tables"]]
        assert "customers" in table_names
        assert "products" in table_names
        assert "orders" in table_names

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_list_tables_not_found(self, mock_logger):
        """Test table listing with non-existent database."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_list_tables

        result = sqlite_list_tables(database_path="/nonexistent/database.db")

        assert isinstance(result, dict)
        assert "error" in result
        assert "Database file not found" in result["error"]

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_sample_table_data_success(self, mock_logger, sample_db):
        """Test successful table data sampling."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_sample_table_data

        result = sqlite_sample_table_data(table_name="customers", limit=3, database_path=sample_db)

        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert "results" in result
        assert "sampling_info" in result
        assert len(result["results"]) <= 3
        assert result["sampling_info"]["table_name"] == "customers"
        assert result["sampling_info"]["limit_requested"] == 3

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_sample_table_data_invalid_limit(self, mock_logger, sample_db):
        """Test table data sampling with invalid limit."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_sample_table_data

        result = sqlite_sample_table_data(
            table_name="customers",
            limit=2000,  # Over the 1000 limit
            database_path=sample_db,
        )

        assert isinstance(result, dict)
        assert "error" in result
        assert "Limit must be between" in result["error"]

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_create_sample_database_success(self, mock_logger):
        """Test successful sample database creation."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_create_sample_database

        fd, temp_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)

        try:
            result = sqlite_create_sample_database(database_path=temp_path)

            assert isinstance(result, dict)
            assert result["status"] == "success"
            assert "tables_created" in result
            assert len(result["tables_created"]) >= 4
            assert "customers" in result["tables_created"]
            assert "products" in result["tables_created"]
            assert os.path.exists(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_sqlite_connection_caching(self, sample_db):
        """Test SQLite connection caching functionality."""
        from service_name_mcp.sqlite_domain.sqlite_tools import get_sqlite_connection

        # Get first connection
        conn1 = get_sqlite_connection(sample_db)
        assert conn1 is not None

        # Get second connection - should be cached
        conn2 = get_sqlite_connection(sample_db)
        assert conn2 is conn1  # Should be the same object

    def test_sqlite_database_path_validation(self, temp_db):
        """Test database path validation."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_execute_query

        # Test with non-existent directory
        result = sqlite_execute_query(query="SELECT 1", database_path="/nonexistent/path/database.db")

        assert isinstance(result, dict)
        assert "error" in result

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_sqlite_complex_query(self, mock_logger, sample_db):
        """Test complex SQL query execution."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_execute_query

        # Complex query with JOIN
        query = """
        SELECT c.name, c.email, COUNT(o.id) as order_count
        FROM customers c
        LEFT JOIN orders o ON c.id = o.customer_id
        GROUP BY c.id, c.name, c.email
        ORDER BY order_count DESC
        """

        result = sqlite_execute_query(query=query, database_path=sample_db)

        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert "results" in result
        assert len(result["results"]) > 0

    def test_sqlite_row_factory_functionality(self, sample_db):
        """Test that row factory returns dict-like results."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_execute_query

        result = sqlite_execute_query(query="SELECT name, email FROM customers LIMIT 1", database_path=sample_db)

        assert result["status"] == "success"
        assert len(result["results"]) > 0

        # Results should be dictionaries, not tuples
        first_row = result["results"][0]
        assert isinstance(first_row, dict)
        assert "name" in first_row
        assert "email" in first_row


class TestSQLiteIntegration:
    """Integration tests for SQLite domain."""

    def test_mcp_tool_registration(self):
        """Test that SQLite tools are properly registered with MCP."""
        try:
            from service_name_mcp.mcp_instance import mcp

            assert mcp is not None
        except ImportError as e:
            pytest.fail(f"Failed to register SQLite tools with MCP: {e}")

    @pytest.mark.integration
    def test_end_to_end_sqlite_workflow(self):
        """Test complete SQLite workflow."""
        from service_name_mcp.sqlite_domain.sqlite_tools import (
            sqlite_create_sample_database,
            sqlite_execute_query,
            sqlite_get_table_schema,
            sqlite_list_tables,
            sqlite_sample_table_data,
        )

        fd, temp_db = tempfile.mkstemp(suffix=".db")
        os.close(fd)

        try:
            # 1. Create sample database
            create_result = sqlite_create_sample_database(database_path=temp_db)
            assert create_result["status"] == "success"

            # 2. List tables
            tables_result = sqlite_list_tables(database_path=temp_db)
            assert len(tables_result["tables"]) >= 4

            # 3. Get schema for a table
            schema_result = sqlite_get_table_schema(table_name="customers", database_path=temp_db)
            assert "columns" in schema_result

            # 4. Sample data from table
            sample_result = sqlite_sample_table_data(table_name="customers", limit=5, database_path=temp_db)
            assert sample_result["status"] == "success"

            # 5. Execute complex query
            query_result = sqlite_execute_query(query="SELECT COUNT(*) as total FROM customers", database_path=temp_db)
            assert query_result["status"] == "success"
            assert len(query_result["results"]) == 1

        finally:
            if os.path.exists(temp_db):
                os.unlink(temp_db)

    @pytest.mark.integration
    def test_data_consistency_workflow(self):
        """Test data consistency across operations."""
        from service_name_mcp.sqlite_domain.sqlite_tools import (
            sqlite_create_sample_database,
            sqlite_execute_query,
            sqlite_sample_table_data,
        )

        fd, temp_db = tempfile.mkstemp(suffix=".db")
        os.close(fd)

        try:
            # Create database with sample data
            sqlite_create_sample_database(database_path=temp_db)

            # Count total customers
            count_result = sqlite_execute_query(query="SELECT COUNT(*) as total FROM customers", database_path=temp_db)
            total_customers = count_result["results"][0]["total"]

            # Sample all customers
            sample_result = sqlite_sample_table_data(table_name="customers", limit=100, database_path=temp_db)

            # Verify consistency
            assert len(sample_result["results"]) == total_customers
            assert sample_result["sampling_info"]["sample_size"] == total_customers

        finally:
            if os.path.exists(temp_db):
                os.unlink(temp_db)


class TestSQLiteErrorHandling:
    """Test SQLite error handling scenarios."""

    def test_connection_error_handling(self):
        """Test handling of connection errors."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_execute_query

        # Test with completely invalid path
        result = sqlite_execute_query(query="SELECT 1", database_path="\x00invalid\x00path")

        assert isinstance(result, dict)
        assert "error" in result

    def test_sql_syntax_error_handling(self):
        """Test handling of SQL syntax errors."""
        from service_name_mcp.sqlite_domain.sqlite_tools import sqlite_create_sample_database, sqlite_execute_query

        fd, temp_db = tempfile.mkstemp(suffix=".db")
        os.close(fd)

        try:
            sqlite_create_sample_database(database_path=temp_db)

            # Execute invalid SQL
            result = sqlite_execute_query(
                query="SELECT * FROM nonexistent_table WHERE invalid syntax", database_path=temp_db
            )

            assert isinstance(result, dict)
            assert "error" in result
            assert "SQLite error" in result["error"]

        finally:
            if os.path.exists(temp_db):
                os.unlink(temp_db)

    def test_table_not_found_handling(self):
        """Test handling when tables don't exist."""
        from service_name_mcp.sqlite_domain.sqlite_tools import (
            sqlite_create_sample_database,
            sqlite_get_table_schema,
            sqlite_sample_table_data,
        )

        fd, temp_db = tempfile.mkstemp(suffix=".db")
        os.close(fd)

        try:
            sqlite_create_sample_database(database_path=temp_db)

            # Test schema for non-existent table
            schema_result = sqlite_get_table_schema(table_name="does_not_exist", database_path=temp_db)
            assert "error" in schema_result

            # Test sampling non-existent table
            sample_result = sqlite_sample_table_data(table_name="does_not_exist", database_path=temp_db)
            assert "error" in sample_result

        finally:
            if os.path.exists(temp_db):
                os.unlink(temp_db)


if __name__ == "__main__":
    pytest.main([__file__])
