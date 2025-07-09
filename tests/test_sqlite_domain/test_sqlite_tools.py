"""
Test suite for SQLite Domain

This module contains unit tests for SQLite database integration tools.
"""

import os
import sqlite3
import tempfile
from unittest.mock import patch

import pytest

# Note: These tests use the template placeholders and will work after setup_template.py is run


class TestSQLiteTools:
    """Test SQLite domain functionality."""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary SQLite database for testing."""
        # Create a temporary file
        db_fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(db_fd)

        # Initialize with test data
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create test tables
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product TEXT,
                amount DECIMAL(10,2),
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # Insert test data
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("John Doe", "john@example.com"))
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Jane Smith", "jane@example.com"))
        cursor.execute("INSERT INTO orders (user_id, product, amount) VALUES (?, ?, ?)", (1, "Widget", 29.99))
        cursor.execute("INSERT INTO orders (user_id, product, amount) VALUES (?, ?, ?)", (2, "Gadget", 49.99))

        conn.commit()
        conn.close()

        yield db_path

        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)

    def test_sqlite_tools_import(self):
        """Test that SQLite tools can be imported."""
        try:
            from service_name_mcp.sqlite_domain import sqlite_tools

            assert sqlite_tools is not None
        except ImportError as e:
            pytest.fail(f"Failed to import SQLite tools: {e}")

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_execute_query_success(self, mock_logger, temp_db):
        """Test successful query execution."""
        from service_name_mcp.sqlite_domain.sqlite_tools import execute_sql_query

        # Test simple SELECT query
        result = execute_sql_query(
            query="SELECT name, email FROM users WHERE id = ?", database_path=temp_db, parameters=(1,)
        )

        assert isinstance(result, list)
        assert len(result) > 0
        assert "John Doe" in str(result)
        mock_logger.info.assert_called()

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_execute_query_with_limit(self, mock_logger, temp_db):
        """Test query execution with result limit."""
        from service_name_mcp.sqlite_domain.sqlite_tools import execute_sql_query

        result = execute_sql_query(query="SELECT * FROM users", database_path=temp_db, limit=1)

        assert isinstance(result, list)
        assert len(result) <= 1

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_execute_query_error_handling(self, mock_logger, temp_db):
        """Test query execution error handling."""
        from service_name_mcp.sqlite_domain.sqlite_tools import execute_sql_query

        # Test invalid SQL
        with pytest.raises(Exception):  # noqa: B017
            execute_sql_query(query="SELECT * FROM nonexistent_table", database_path=temp_db)

        mock_logger.error.assert_called()

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_get_schema_info(self, mock_logger, temp_db):
        """Test schema information retrieval."""
        from service_name_mcp.sqlite_domain.sqlite_tools import get_schema_info

        result = get_schema_info(database_path=temp_db)

        assert isinstance(result, dict)
        assert "tables" in result
        assert len(result["tables"]) > 0

        # Check that our test tables are present
        table_names = [table["name"] for table in result["tables"]]
        assert "users" in table_names
        assert "orders" in table_names

    @patch("service_name_mcp.sqlite_domain.sqlite_tools.logger")
    def test_get_table_sample(self, mock_logger, temp_db):
        """Test table data sampling."""
        from service_name_mcp.sqlite_domain.sqlite_tools import get_table_sample

        result = get_table_sample(table_name="users", database_path=temp_db, sample_size=5)

        assert isinstance(result, list)
        assert len(result) <= 5
        # Should have our test data
        assert len(result) == 2  # We inserted 2 users

    def test_database_path_validation(self, temp_db):
        """Test database path validation."""
        from service_name_mcp.sqlite_domain.sqlite_tools import execute_sql_query

        # Test with non-existent database
        with pytest.raises(Exception):  # noqa: B017
            execute_sql_query(query="SELECT 1", database_path="/nonexistent/path/db.sqlite")

    def test_sql_injection_protection(self, temp_db):
        """Test SQL injection protection through parameterized queries."""
        from service_name_mcp.sqlite_domain.sqlite_tools import execute_sql_query

        # This should work safely with parameters
        malicious_input = "'; DROP TABLE users; --"
        result = execute_sql_query(
            query="SELECT * FROM users WHERE name = ?", database_path=temp_db, parameters=(malicious_input,)
        )

        # Should return empty result, not cause error
        assert isinstance(result, list)
        assert len(result) == 0

        # Verify table still exists
        schema = execute_sql_query(
            query="SELECT name FROM sqlite_master WHERE type='table' AND name='users'", database_path=temp_db
        )
        assert len(schema) == 1


class TestSQLiteBestPractices:
    """Test SQLite best practices and documentation."""

    def test_best_practices_file_exists(self):
        """Test that best practices documentation exists."""
        from pathlib import Path

        # Get the path to the best practices file
        current_dir = Path(__file__).parent.parent.parent
        best_practices_path = current_dir / "src" / "service_name_mcp" / "sqlite_domain" / "best_practices.md"

        assert best_practices_path.exists(), "SQLite best practices file should exist"

        # Verify it has content
        content = best_practices_path.read_text()
        assert len(content) > 100, "Best practices should have substantial content"
        assert "SQLite" in content, "Best practices should mention SQLite"


# Integration tests
class TestSQLiteIntegration:
    """Integration tests for SQLite domain."""

    def test_mcp_tool_registration(self):
        """Test that SQLite tools are properly registered with MCP."""
        try:
            # Import the tools module to trigger registration
            from service_name_mcp.mcp_instance import mcp

            # This test verifies that import doesn't fail
            # The actual tool registration testing would require MCP framework testing
            assert mcp is not None

        except ImportError as e:
            pytest.fail(f"Failed to register SQLite tools with MCP: {e}")

    @pytest.mark.integration
    def test_end_to_end_workflow(self, temp_db):
        """Test complete SQLite workflow."""
        from service_name_mcp.sqlite_domain.sqlite_tools import execute_sql_query, get_schema_info, get_table_sample

        # 1. Get schema
        schema = get_schema_info(database_path=temp_db)
        assert "tables" in schema

        # 2. Sample data from a table
        sample = get_table_sample(table_name="users", database_path=temp_db)
        assert len(sample) > 0

        # 3. Execute analytical query
        result = execute_sql_query(
            query="""
                SELECT u.name, COUNT(o.id) as order_count, SUM(o.amount) as total_spent
                FROM users u
                LEFT JOIN orders o ON u.id = o.user_id
                GROUP BY u.id, u.name
                ORDER BY total_spent DESC
            """,
            database_path=temp_db,
        )

        assert len(result) > 0
        assert isinstance(result[0], tuple)


if __name__ == "__main__":
    pytest.main([__file__])
