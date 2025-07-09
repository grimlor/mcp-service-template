# SQLite Domain Best Practices

## Overview
The SQLite domain demonstrates database integration patterns using SQLite, a free, serverless database engine available on virtually every platform. This domain is perfect for learning database integration without requiring external services or complex setup.

## Key Learning Objectives

### 1. **Database Connection Management**
- Connection caching and reuse
- Proper connection lifecycle management
- Error handling for database connectivity issues

### 2. **Query Execution Patterns**
- Safe query execution with error handling
- Different handling for SELECT vs. modification queries
- Result formatting and metadata extraction

### 3. **Schema Introspection**
- Dynamic schema discovery
- Table listing and metadata extraction
- Foreign key and index analysis

### 4. **Data Sampling and Exploration**
- Safe data sampling with limits
- Result formatting for analysis
- Performance considerations for large datasets

## Tool Usage Examples

### Basic Query Execution
```python
# Execute a simple SELECT query
result = sqlite_execute_query(
    "SELECT * FROM customers WHERE city = 'New York'",
    "./data/sample.db"
)

# Execute aggregation query
result = sqlite_execute_query(
    "SELECT category, COUNT(*), AVG(price) FROM products GROUP BY category"
)
```

### Schema Exploration
```python
# List all tables
tables = sqlite_list_tables("./data/sample.db")

# Get schema for specific table
schema = sqlite_get_table_schema("customers", "./data/sample.db")

# Sample data from table
sample = sqlite_sample_table_data("orders", limit=20)
```

### Database Setup
```python
# Create sample database for learning
result = sqlite_create_sample_database("./learning/ecommerce.db")
```

## Security Best Practices

### 1. **Input Validation**
- Always validate table names and query structure
- Use parameterized queries when building dynamic SQL
- Limit query complexity and execution time

### 2. **File Access Control**
- Validate database file paths
- Restrict access to authorized directories
- Handle file permission errors gracefully

### 3. **Resource Management**
- Implement connection pooling and cleanup
- Set reasonable limits on result set sizes
- Monitor memory usage for large queries

## Performance Considerations

### 1. **Connection Caching**
- Cache connections to avoid repeated overhead
- Implement connection validation and recovery
- Monitor connection pool health

### 2. **Query Optimization**
- Use EXPLAIN QUERY PLAN for complex queries
- Implement query result caching where appropriate
- Set reasonable timeouts for long-running queries

### 3. **Memory Management**
- Limit result set sizes to prevent memory exhaustion
- Use pagination for large datasets
- Stream results when possible

## Error Handling Patterns

### 1. **Database Errors**
```python
try:
    result = sqlite_execute_query(query)
except sqlite3.Error as e:
    # Handle SQLite-specific errors
    return {"error": f"Database error: {str(e)}"}
except Exception as e:
    # Handle unexpected errors
    return {"error": f"Unexpected error: {str(e)}"}
```

### 2. **File System Errors**
```python
if not os.path.exists(db_path):
    return {"error": f"Database file not found: {db_path}"}
```

### 3. **Validation Errors**
```python
if limit < 1 or limit > 1000:
    return {"error": "Limit must be between 1 and 1000"}
```

## Common Use Cases

### 1. **Data Analysis**
- Explore datasets stored in SQLite format
- Perform aggregations and statistical analysis
- Generate reports from local data

### 2. **Application Data**
- Access application databases
- Analyze user behavior data
- Debug data-related issues

### 3. **Learning and Prototyping**
- Practice SQL queries in a safe environment
- Test database schema designs
- Learn database optimization techniques

## Integration with Other Domains

### 1. **CSV Domain Integration**
- Import CSV data into SQLite for analysis
- Export SQLite results to CSV format
- Combine file processing with database operations

### 2. **REST API Domain Integration**
- Store API responses in SQLite for caching
- Use SQLite as a local data warehouse
- Implement data synchronization patterns

### 3. **Analytics Domain Integration**
- Use SQLite as data source for analytics tools
- Store analysis results for historical tracking
- Implement data pipelines with SQLite staging

## Advanced Patterns

### 1. **Dynamic Query Building**
```python
def build_customer_query(filters):
    where_clauses = []
    if filters.get('city'):
        where_clauses.append(f"city = '{filters['city']}'")
    if filters.get('active_only'):
        where_clauses.append("is_active = 1")
    
    base_query = "SELECT * FROM customers"
    if where_clauses:
        base_query += " WHERE " + " AND ".join(where_clauses)
    
    return base_query
```

### 2. **Batch Operations**
```python
def batch_insert_data(table_name, records):
    placeholders = ",".join(["?" for _ in records[0].keys()])
    query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    
    conn.executemany(query, [list(record.values()) for record in records])
    conn.commit()
```

### 3. **Schema Migration**
```python
def migrate_schema(db_path, migrations):
    for migration in migrations:
        sqlite_execute_query(migration, db_path)
```

## Debugging and Troubleshooting

### 1. **Query Analysis**
- Use EXPLAIN QUERY PLAN to understand query execution
- Monitor query execution time
- Analyze result set sizes and structure

### 2. **Connection Issues**
- Verify database file exists and is readable
- Check file permissions and ownership
- Validate SQLite database format

### 3. **Performance Issues**
- Monitor memory usage during large queries
- Implement query timeouts
- Use VACUUM to optimize database file

## Learning Exercises

### 1. **Basic Operations**
1. Create a sample database with the provided tool
2. Practice different types of SELECT queries
3. Experiment with JOINs across multiple tables
4. Try aggregation functions and GROUP BY clauses

### 2. **Schema Analysis**
1. Explore the schema of different tables
2. Understand foreign key relationships
3. Analyze indexes and their purposes
4. Practice PRAGMA commands for metadata

### 3. **Data Manipulation**
1. Practice INSERT, UPDATE, DELETE operations
2. Implement data validation rules
3. Work with transactions and rollbacks
4. Learn about data types and constraints

### 4. **Advanced Queries**
1. Write complex queries with subqueries
2. Use window functions for analytics
3. Implement full-text search
4. Practice query optimization techniques

This SQLite domain provides a comprehensive foundation for database integration patterns that can be applied to any SQL database system, while requiring no external services or complex setup.
