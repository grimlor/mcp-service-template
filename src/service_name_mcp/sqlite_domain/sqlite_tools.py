"""
SQLite Database Integration Tools

This domain demonstrates integration with SQLite databases, which are free,
lightweight, and available on any system. Perfect for learning database
integration patterns without requiring external services.

Key Patterns Demonstrated:
- Database connection management
- Query execution and result formatting
- Error handling and validation
- Schema introspection
- Data sampling and exploration
"""

import os
import sqlite3
from typing import Any

from ..common.config import Config
from ..common.logging import get_logger
from ..mcp_instance import mcp

logger = get_logger(__name__)

# Global connection cache
_connection_cache = {}


def get_sqlite_connection(db_path: str) -> sqlite3.Connection:
    """Get cached SQLite connection"""
    if db_path not in _connection_cache:
        try:
            # Enable row factory for dict-like results
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            _connection_cache[db_path] = conn
            logger.info(f"Created new SQLite connection to {db_path}")
        except Exception as e:
            logger.error(f"Failed to connect to SQLite database {db_path}: {str(e)}")
            raise

    return _connection_cache[db_path]


@mcp.tool(description="Execute SQL query against SQLite database")
def sqlite_execute_query(query: str, database_path: str | None = None) -> dict[str, Any]:
    """
    Execute a SQL query against a SQLite database.

    Args:
        query: SQL query to execute
        database_path: Path to SQLite database file (optional, uses default if not provided)

    Returns:
        Dictionary containing query results and metadata
    """
    # Use default database path if not provided
    db_path: str = database_path or str(getattr(Config, "DEFAULT_SQLITE_DB", "./data/sample.db"))

    try:
        # Validate database exists
        if not os.path.exists(db_path):
            return {
                "error": f"Database file not found: {db_path}",
                "suggestion": "Create a sample database or provide a valid database_path",
            }

        conn = get_sqlite_connection(db_path)
        cursor = conn.cursor()

        # Execute query
        cursor.execute(query)

        # Handle different query types
        if query.strip().upper().startswith(("SELECT", "WITH", "EXPLAIN")):
            # Query returns results
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]

            return {
                "status": "success",
                "query": query,
                "database": db_path,
                "results": results,
                "row_count": len(results),
                "columns": [desc[0] for desc in cursor.description] if cursor.description else [],
            }
        else:
            # Query modifies data
            conn.commit()
            return {
                "status": "success",
                "query": query,
                "database": db_path,
                "rows_affected": cursor.rowcount,
                "message": "Query executed successfully",
            }

    except sqlite3.Error as e:
        logger.error(f"SQLite query error: {str(e)}")
        return {
            "error": f"SQLite error: {str(e)}",
            "query": query,
            "database": db_path,
        }
    except Exception as e:
        logger.error(f"Unexpected error executing SQLite query: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}", "query": query}


@mcp.tool(description="Get schema information for SQLite database tables")
def sqlite_get_table_schema(table_name: str, database_path: str | None = None) -> dict[str, Any]:
    """
    Get detailed schema information for a specific table.

    Args:
        table_name: Name of the table to inspect
        database_path: Path to SQLite database file

    Returns:
        Dictionary containing table schema information
    """
    try:
        db_path: str = database_path or str(getattr(Config, "DEFAULT_SQLITE_DB", "./data/sample.db"))

        if not os.path.exists(db_path):
            return {"error": f"Database file not found: {db_path}"}

        conn = get_sqlite_connection(db_path)
        cursor = conn.cursor()

        # Get table info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        if not columns:
            return {"error": f"Table '{table_name}' not found"}

        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = cursor.fetchall()

        # Get indexes
        cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = cursor.fetchall()

        schema_info = {
            "table_name": table_name,
            "database": db_path,
            "columns": [dict(col) for col in columns],
            "foreign_keys": [dict(fk) for fk in foreign_keys],
            "indexes": [dict(idx) for idx in indexes],
            "column_count": len(columns),
        }

        logger.info(f"Retrieved schema for table {table_name}")
        return schema_info

    except sqlite3.Error as e:
        logger.error(f"SQLite schema error: {str(e)}")
        return {"error": f"SQLite error: {str(e)}"}


@mcp.tool(description="List all tables in SQLite database")
def sqlite_list_tables(database_path: str | None = None) -> dict[str, Any]:
    """
    List all tables in the SQLite database.

    Args:
        database_path: Path to SQLite database file

    Returns:
        Dictionary containing list of tables and metadata
    """
    try:
        db_path: str = database_path or str(getattr(Config, "DEFAULT_SQLITE_DB", "./data/sample.db"))

        if not os.path.exists(db_path):
            return {"error": f"Database file not found: {db_path}"}

        conn = get_sqlite_connection(db_path)
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("""
            SELECT name, type, sql
            FROM sqlite_master
            WHERE type IN ('table', 'view')
            ORDER BY name
        """)

        tables = cursor.fetchall()
        table_list = []

        for table in tables:
            # Get row count for each table
            if table["type"] == "table":
                cursor.execute(f"SELECT COUNT(*) as count FROM {table['name']}")
                row_count = cursor.fetchone()["count"]
            else:
                row_count = None

            table_list.append(
                {"name": table["name"], "type": table["type"], "row_count": row_count, "sql": table["sql"]}
            )

        return {"database": db_path, "tables": table_list, "table_count": len(table_list)}

    except sqlite3.Error as e:
        logger.error(f"SQLite list tables error: {str(e)}")
        return {"error": f"SQLite error: {str(e)}"}


@mcp.tool(description="Get sample data from SQLite table")
def sqlite_sample_table_data(table_name: str, limit: int = 10, database_path: str | None = None) -> dict[str, Any]:
    """
    Get sample data from a table for exploration.

    Args:
        table_name: Name of the table to sample
        limit: Maximum number of rows to return
        database_path: Path to SQLite database file

    Returns:
        Dictionary containing sample data and metadata
    """
    try:
        db_path: str = database_path or str(getattr(Config, "DEFAULT_SQLITE_DB", "./data/sample.db"))

        if not os.path.exists(db_path):
            return {"error": f"Database file not found: {db_path}"}

        # Validate limit
        if limit < 1 or limit > 1000:
            return {"error": "Limit must be between 1 and 1000"}

        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        result: dict[str, Any] = sqlite_execute_query(query, db_path)

        if "error" in result:
            return result

        # Add sampling metadata
        result["sampling_info"] = {
            "table_name": table_name,
            "sample_size": len(result.get("results", [])),
            "limit_requested": limit,
        }

        return result

    except Exception as e:
        logger.error(f"Error sampling table data: {str(e)}")
        return {"error": f"Sampling error: {str(e)}"}


@mcp.tool(description="Create sample SQLite database with demo data")
def sqlite_create_sample_database(database_path: str | None = None) -> dict[str, Any]:
    """
    Create a sample SQLite database with demo data for learning purposes.

    Args:
        database_path: Path where to create the sample database

    Returns:
        Dictionary containing creation results
    """
    try:
        db_path = database_path or "./data/sample.db"

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Create connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create sample tables
        cursor.executescript("""
            -- Customers table
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                city TEXT,
                signup_date DATE,
                is_active BOOLEAN DEFAULT 1
            );

            -- Products table
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                price DECIMAL(10,2),
                stock_quantity INTEGER DEFAULT 0
            );

            -- Orders table
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                order_date DATE,
                total_amount DECIMAL(10,2),
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            );

            -- Order items table
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                unit_price DECIMAL(10,2),
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            );
        """)

        # Insert sample data
        cursor.executescript("""
            -- Sample customers
            INSERT OR REPLACE INTO customers (name, email, city, signup_date) VALUES
            ('Alice Johnson', 'alice@example.com', 'New York', '2024-01-15'),
            ('Bob Smith', 'bob@example.com', 'Los Angeles', '2024-02-20'),
            ('Carol Davis', 'carol@example.com', 'Chicago', '2024-03-10'),
            ('David Wilson', 'david@example.com', 'Houston', '2024-04-05'),
            ('Eva Brown', 'eva@example.com', 'Phoenix', '2024-05-12');

            -- Sample products
            INSERT OR REPLACE INTO products (name, category, price, stock_quantity) VALUES
            ('Laptop Pro', 'Electronics', 1299.99, 50),
            ('Wireless Mouse', 'Electronics', 29.99, 200),
            ('Office Chair', 'Furniture', 249.99, 30),
            ('Coffee Mug', 'Kitchen', 12.99, 100),
            ('Notebook Set', 'Office', 15.99, 150);

            -- Sample orders
            INSERT OR REPLACE INTO orders (customer_id, order_date, total_amount, status) VALUES
            (1, '2024-06-01', 1329.98, 'completed'),
            (2, '2024-06-05', 29.99, 'completed'),
            (3, '2024-06-10', 262.98, 'shipped'),
            (4, '2024-06-15', 28.98, 'pending'),
            (1, '2024-06-20', 15.99, 'completed');

            -- Sample order items
            INSERT OR REPLACE INTO order_items (order_id, product_id, quantity, unit_price) VALUES
            (1, 1, 1, 1299.99),
            (1, 2, 1, 29.99),
            (2, 2, 1, 29.99),
            (3, 3, 1, 249.99),
            (3, 5, 1, 12.99),
            (4, 4, 2, 12.99),
            (4, 5, 1, 15.99),
            (5, 5, 1, 15.99);
        """)

        conn.commit()
        conn.close()

        # Update cache if this is the default database
        if db_path in _connection_cache:
            del _connection_cache[db_path]

        return {
            "status": "success",
            "message": "Sample database created successfully",
            "database_path": db_path,
            "tables_created": ["customers", "products", "orders", "order_items"],
            "sample_data": "Demo e-commerce data inserted",
        }

    except Exception as e:
        logger.error(f"Error creating sample database: {str(e)}")
        return {"error": f"Database creation failed: {str(e)}"}
