"""
File Processing Tools

This domain demonstrates file processing patterns for CSV, JSON, and text files.
Uses only standard library and common packages available everywhere.

Key Patterns Demonstrated:
- File I/O operations with proper error handling
- CSV processing and data transformation
- JSON file manipulation
- Text file analysis and processing
- Directory operations and file discovery
"""

import csv
import glob
import json
import os
import re
from datetime import datetime
from typing import Any

# from ..common.config import Config  # TODO: Remove if not using config
from ..common.logging import get_logger
from ..mcp_instance import mcp

logger = get_logger(__name__)


@mcp.tool(description="Read and analyze CSV file")
def read_csv_file(
    file_path: str, delimiter: str = ",", has_header: bool = True, max_rows: int = 1000, encoding: str = "utf-8"
) -> dict[str, Any]:
    """
    Read and analyze a CSV file with various options.

    Args:
        file_path: Path to the CSV file
        delimiter: CSV delimiter character
        has_header: Whether the first row contains column headers
        max_rows: Maximum number of rows to read
        encoding: File encoding

    Returns:
        Dictionary containing CSV data and analysis
    """
    try:
        # Validate file exists
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        # Validate file size (prevent loading huge files)
        file_size = os.path.getsize(file_path)
        if file_size > 50 * 1024 * 1024:  # 50MB limit
            return {"error": f"File too large: {file_size} bytes (max 50MB)"}

        rows = []
        headers = None

        with open(file_path, encoding=encoding, newline="") as csvfile:
            # Detect dialect
            sample = csvfile.read(1024)
            csvfile.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=delimiter)
                reader = csv.reader(csvfile, dialect)
            except csv.Error:
                # Fall back to manual delimiter
                reader = csv.reader(csvfile, delimiter=delimiter)

            # Read headers if present
            if has_header:
                try:
                    headers = next(reader)
                except StopIteration:
                    return {"error": "Empty CSV file"}

            # Read data rows
            row_count = 0
            for row in reader:
                if row_count >= max_rows:
                    break
                rows.append(row)
                row_count += 1

        # Analyze data
        analysis: dict[str, Any] = {
            "file_info": {"path": file_path, "size_bytes": file_size, "encoding": encoding, "delimiter": delimiter},
            "structure": {
                "total_rows_read": len(rows),
                "has_header": has_header,
                "headers": headers,
                "column_count": len(headers) if headers else (len(rows[0]) if rows else 0),
                "max_rows_limit": max_rows,
            },
            "data": [],
        }

        # Convert rows to dictionaries if headers available
        if headers and rows:
            for row in rows:
                if len(row) == len(headers):
                    analysis["data"].append(dict(zip(headers, row, strict=False)))
                else:
                    # Handle rows with different column counts
                    row_dict = {}
                    for i, header in enumerate(headers):
                        row_dict[header] = row[i] if i < len(row) else ""
                    analysis["data"].append(row_dict)
        else:
            # No headers, use raw rows
            analysis["data"] = [{"row_" + str(i): value for i, value in enumerate(row)} for row in rows]

        # Add column analysis
        if analysis["data"]:
            analysis["column_analysis"] = analyze_csv_columns(analysis["data"], headers)

        logger.info(f"Successfully read CSV file: {file_path} ({len(rows)} rows)")
        return analysis

    except UnicodeDecodeError as e:
        return {"error": f"Encoding error: {str(e)}. Try different encoding."}
    except Exception as e:
        logger.error(f"Error reading CSV file: {str(e)}")
        return {"error": f"Failed to read CSV: {str(e)}"}


def analyze_csv_columns(data: list[dict[str, Any]], headers: list[str] | None) -> dict[str, Any]:
    """Analyze CSV columns for data types and patterns"""
    if not data:
        return {}

    column_analysis = {}
    columns = headers if headers else list(data[0].keys())

    for col in columns:
        values = [row.get(col, "") for row in data if row.get(col, "").strip()]

        analysis = {
            "total_values": len([row.get(col, "") for row in data]),
            "non_empty_values": len(values),
            "empty_values": len(data) - len(values),
            "unique_values": len(set(values)),
            "sample_values": list(set(values))[:5],
        }

        # Detect data types
        if values:
            numeric_count = 0
            date_count = 0

            for value in values[:100]:  # Sample first 100 values
                # Check if numeric
                try:
                    float(value)
                    numeric_count += 1
                except ValueError:
                    pass

                # Check if date-like
                if re.match(r"\d{4}-\d{2}-\d{2}", value) or re.match(r"\d{2}/\d{2}/\d{4}", value):
                    date_count += 1

            total_checked = min(len(values), 100)
            analysis["likely_numeric"] = numeric_count / total_checked > 0.8
            analysis["likely_date"] = date_count / total_checked > 0.8

        column_analysis[col] = analysis

    return column_analysis


@mcp.tool(description="Write data to CSV file")
def write_csv_file(
    file_path: str, data: list[dict[str, Any]], delimiter: str = ",", encoding: str = "utf-8"
) -> dict[str, Any]:
    """
    Write data to a CSV file.

    Args:
        file_path: Path where to save the CSV file
        data: List of dictionaries to write as CSV
        delimiter: CSV delimiter character
        encoding: File encoding

    Returns:
        Dictionary containing write operation results
    """
    try:
        if not data:
            return {"error": "No data provided to write"}

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Get headers from first row
        headers = list(data[0].keys())

        with open(file_path, "w", encoding=encoding, newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)

        file_size = os.path.getsize(file_path)

        result = {
            "status": "success",
            "file_path": file_path,
            "rows_written": len(data),
            "columns": len(headers),
            "file_size_bytes": file_size,
            "encoding": encoding,
            "delimiter": delimiter,
        }

        logger.info(f"Successfully wrote CSV file: {file_path} ({len(data)} rows)")
        return result

    except Exception as e:
        logger.error(f"Error writing CSV file: {str(e)}")
        return {"error": f"Failed to write CSV: {str(e)}"}


@mcp.tool(description="Read and parse JSON file")
def read_json_file(file_path: str, encoding: str = "utf-8") -> dict[str, Any]:
    """
    Read and parse a JSON file.

    Args:
        file_path: Path to the JSON file
        encoding: File encoding

    Returns:
        Dictionary containing JSON data and metadata
    """
    try:
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        file_size = os.path.getsize(file_path)
        if file_size > 100 * 1024 * 1024:  # 100MB limit
            return {"error": f"File too large: {file_size} bytes (max 100MB)"}

        with open(file_path, encoding=encoding) as jsonfile:
            data = json.load(jsonfile)

        result = {
            "file_info": {"path": file_path, "size_bytes": file_size, "encoding": encoding},
            "data": data,
            "analysis": analyze_json_structure(data),
        }

        logger.info(f"Successfully read JSON file: {file_path}")
        return result

    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON format: {str(e)}"}
    except UnicodeDecodeError as e:
        return {"error": f"Encoding error: {str(e)}"}
    except Exception as e:
        logger.error(f"Error reading JSON file: {str(e)}")
        return {"error": f"Failed to read JSON: {str(e)}"}


def analyze_json_structure(data: Any, max_depth: int = 5) -> dict[str, Any]:
    """Analyze JSON structure and provide metadata"""

    def get_structure(obj: Any, depth: int = 0) -> Any:
        if depth > max_depth:
            return "..."

        if isinstance(obj, dict):
            if not obj:
                return "empty_dict"

            structure = {}
            for key, value in list(obj.items())[:10]:  # Sample first 10 keys
                structure[key] = get_structure(value, depth + 1)

            if len(obj) > 10:
                structure["..."] = f"and {len(obj) - 10} more keys"

            return structure
        elif isinstance(obj, list):
            if not obj:
                return "empty_list"

            # Analyze first few items
            samples = [get_structure(item, depth + 1) for item in obj[:3]]

            return {
                "array_length": len(obj),
                "sample_items": samples,
                "all_same_type": len({type(item).__name__ for item in obj}) == 1,
            }
        else:
            return type(obj).__name__

    return {"type": type(data).__name__, "structure": get_structure(data), "size_estimate": estimate_json_size(data)}


def estimate_json_size(obj: Any) -> dict[str, int]:
    """Estimate size characteristics of JSON object"""

    def count_elements(obj: Any) -> int:
        if isinstance(obj, dict):
            return sum(count_elements(v) for v in obj.values()) + len(obj)
        elif isinstance(obj, list):
            return sum(count_elements(item) for item in obj) + len(obj)
        else:
            return 1

    return {"total_elements": count_elements(obj), "depth": get_json_depth(obj)}


def get_json_depth(obj: Any, current_depth: int = 0) -> int:
    """Calculate maximum depth of JSON object"""
    if isinstance(obj, dict):
        if not obj:
            return current_depth
        return max((get_json_depth(v, current_depth + 1) for v in obj.values()), default=current_depth)
    elif isinstance(obj, list):
        if not obj:
            return current_depth
        return max((get_json_depth(item, current_depth + 1) for item in obj), default=current_depth)
    else:
        return current_depth


@mcp.tool(description="Write data to JSON file")
def write_json_file(file_path: str, data: Any, indent: int = 2, encoding: str = "utf-8") -> dict[str, Any]:
    """
    Write data to a JSON file.

    Args:
        file_path: Path where to save the JSON file
        data: Data to write as JSON
        indent: JSON indentation for pretty printing
        encoding: File encoding

    Returns:
        Dictionary containing write operation results
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding=encoding) as jsonfile:
            json.dump(data, jsonfile, indent=indent, ensure_ascii=False)

        file_size = os.path.getsize(file_path)

        result = {
            "status": "success",
            "file_path": file_path,
            "file_size_bytes": file_size,
            "encoding": encoding,
            "indent": indent,
            "data_analysis": analyze_json_structure(data),
        }

        logger.info(f"Successfully wrote JSON file: {file_path}")
        return result

    except Exception as e:
        logger.error(f"Error writing JSON file: {str(e)}")
        return {"error": f"Failed to write JSON: {str(e)}"}


@mcp.tool(description="Analyze text file content")
def analyze_text_file(file_path: str, encoding: str = "utf-8", max_lines: int = 10000) -> dict[str, Any]:
    """
    Analyze a text file and provide statistics.

    Args:
        file_path: Path to the text file
        encoding: File encoding
        max_lines: Maximum number of lines to analyze

    Returns:
        Dictionary containing text analysis results
    """
    try:
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        file_size = os.path.getsize(file_path)
        if file_size > 50 * 1024 * 1024:  # 50MB limit
            return {"error": f"File too large: {file_size} bytes (max 50MB)"}

        lines = []
        with open(file_path, encoding=encoding) as textfile:
            for i, line in enumerate(textfile):
                if i >= max_lines:
                    break
                lines.append(line.rstrip("\n\r"))

        # Perform analysis
        total_chars = sum(len(line) for line in lines)
        total_words = sum(len(line.split()) for line in lines)

        # Character frequency analysis
        char_freq: dict[str, int] = {}
        for line in lines:
            for char in line.lower():
                if char.isalpha():
                    char_freq[char] = char_freq.get(char, 0) + 1

        # Most common words
        word_freq: dict[str, int] = {}
        for line in lines:
            words = re.findall(r"\b\w+\b", line.lower())
            for word in words:
                if len(word) > 2:  # Skip very short words
                    word_freq[word] = word_freq.get(word, 0) + 1

        common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

        analysis = {
            "file_info": {"path": file_path, "size_bytes": file_size, "encoding": encoding},
            "statistics": {
                "total_lines": len(lines),
                "total_characters": total_chars,
                "total_words": total_words,
                "average_line_length": total_chars / len(lines) if lines else 0,
                "average_words_per_line": total_words / len(lines) if lines else 0,
                "max_lines_analyzed": max_lines,
            },
            "content_analysis": {
                "common_words": common_words,
                "character_frequency": sorted(char_freq.items(), key=lambda x: x[1], reverse=True)[:10],
                "empty_lines": sum(1 for line in lines if not line.strip()),
                "longest_line_length": max(len(line) for line in lines) if lines else 0,
            },
            "sample_lines": lines[:5] if lines else [],
        }

        logger.info(f"Successfully analyzed text file: {file_path} ({len(lines)} lines)")
        return analysis

    except UnicodeDecodeError as e:
        return {"error": f"Encoding error: {str(e)}"}
    except Exception as e:
        logger.error(f"Error analyzing text file: {str(e)}")
        return {"error": f"Failed to analyze text: {str(e)}"}


@mcp.tool(description="List files in directory with filtering")
def list_directory_files(
    directory_path: str, pattern: str = "*", include_subdirs: bool = False, file_types: list[str] | None = None
) -> dict[str, Any]:
    """
    List files in a directory with optional filtering.

    Args:
        directory_path: Path to the directory
        pattern: Glob pattern for filtering files
        include_subdirs: Whether to search subdirectories recursively
        file_types: List of file extensions to include (e.g., ['.csv', '.json'])

    Returns:
        Dictionary containing file listing and metadata
    """
    try:
        if not os.path.exists(directory_path):
            return {"error": f"Directory not found: {directory_path}"}

        if not os.path.isdir(directory_path):
            return {"error": f"Path is not a directory: {directory_path}"}

        # Build search pattern
        if include_subdirs:
            search_pattern = os.path.join(directory_path, "**", pattern)
            files = glob.glob(search_pattern, recursive=True)
        else:
            search_pattern = os.path.join(directory_path, pattern)
            files = glob.glob(search_pattern)

        # Filter by file types if specified
        if file_types:
            file_types = [ext.lower() if ext.startswith(".") else "." + ext.lower() for ext in file_types]
            files = [f for f in files if any(f.lower().endswith(ext) for ext in file_types)]

        # Get file information
        file_info = []
        total_size = 0

        for file_path in files:
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                size = stat.st_size
                total_size += size

                file_info.append(
                    {
                        "name": os.path.basename(file_path),
                        "path": file_path,
                        "size_bytes": size,
                        "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "extension": os.path.splitext(file_path)[1].lower(),
                    }
                )

        # Sort by name
        file_info.sort(key=lambda x: str(x["name"]))

        # Group by extension
        extensions: dict[str, dict[str, int]] = {}
        for file in file_info:
            ext = str(file["extension"]) or "no_extension"
            if ext not in extensions:
                extensions[ext] = {"count": 0, "total_size": 0}
            extensions[ext]["count"] += 1
            extensions[ext]["total_size"] += int(str(file["size_bytes"]))

        result = {
            "directory": directory_path,
            "search_pattern": pattern,
            "include_subdirs": include_subdirs,
            "file_types_filter": file_types,
            "summary": {"total_files": len(file_info), "total_size_bytes": total_size, "extensions": extensions},
            "files": file_info,
        }

        logger.info(f"Listed directory: {directory_path} ({len(file_info)} files)")
        return result

    except Exception as e:
        logger.error(f"Error listing directory: {str(e)}")
        return {"error": f"Failed to list directory: {str(e)}"}


@mcp.tool(description="Create sample data files for testing")
def create_sample_files(output_directory: str = "./sample_data") -> dict[str, Any]:
    """
    Create sample CSV, JSON, and text files for testing and learning.

    Args:
        output_directory: Directory where to create sample files

    Returns:
        Dictionary containing creation results
    """
    try:
        # Create output directory
        os.makedirs(output_directory, exist_ok=True)

        files_created = []

        # 1. Sample CSV file - Customer data
        csv_data = [
            {
                "customer_id": 1,
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "age": 29,
                "city": "New York",
                "purchase_amount": 156.78,
            },
            {
                "customer_id": 2,
                "name": "Bob Smith",
                "email": "bob@example.com",
                "age": 35,
                "city": "Los Angeles",
                "purchase_amount": 89.99,
            },
            {
                "customer_id": 3,
                "name": "Carol Davis",
                "email": "carol@example.com",
                "age": 42,
                "city": "Chicago",
                "purchase_amount": 234.56,
            },
            {
                "customer_id": 4,
                "name": "David Wilson",
                "email": "david@example.com",
                "age": 28,
                "city": "Houston",
                "purchase_amount": 45.00,
            },
            {
                "customer_id": 5,
                "name": "Eva Brown",
                "email": "eva@example.com",
                "age": 31,
                "city": "Phoenix",
                "purchase_amount": 378.90,
            },
        ]

        csv_path = os.path.join(output_directory, "customers.csv")
        csv_result = write_csv_file(csv_path, csv_data)
        if "error" not in csv_result:
            files_created.append({"file": "customers.csv", "type": "CSV", "path": csv_path})

        # 2. Sample JSON file - Product catalog
        json_data = {
            "catalog": {
                "name": "Sample Product Catalog",
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "categories": [
                    {
                        "id": 1,
                        "name": "Electronics",
                        "products": [
                            {"id": 101, "name": "Laptop Pro", "price": 1299.99, "in_stock": True},
                            {"id": 102, "name": "Wireless Mouse", "price": 29.99, "in_stock": True},
                            {"id": 103, "name": "USB-C Hub", "price": 79.99, "in_stock": False},
                        ],
                    },
                    {
                        "id": 2,
                        "name": "Books",
                        "products": [
                            {"id": 201, "name": "Python Programming", "price": 39.99, "in_stock": True},
                            {"id": 202, "name": "Data Science Handbook", "price": 49.99, "in_stock": True},
                        ],
                    },
                ],
            },
            "metadata": {"total_categories": 2, "total_products": 5, "currency": "USD"},
        }

        json_path = os.path.join(output_directory, "product_catalog.json")
        json_result = write_json_file(json_path, json_data)
        if "error" not in json_result:
            files_created.append({"file": "product_catalog.json", "type": "JSON", "path": json_path})

        # 3. Sample text file - Log data
        log_content = """2024-01-15 10:30:00 INFO User alice@example.com logged in successfully
2024-01-15 10:31:23 INFO User alice@example.com viewed product catalog
2024-01-15 10:35:45 INFO User alice@example.com added item 101 to cart
2024-01-15 10:36:12 WARN User alice@example.com payment validation failed
2024-01-15 10:36:45 INFO User alice@example.com payment validation succeeded
2024-01-15 10:37:00 INFO Order 12345 created for user alice@example.com
2024-01-15 11:15:30 INFO User bob@example.com logged in successfully
2024-01-15 11:16:45 ERROR Database connection timeout
2024-01-15 11:17:00 INFO Database connection restored
2024-01-15 11:18:23 INFO User bob@example.com searched for "wireless mouse"
2024-01-15 11:19:45 INFO User bob@example.com viewed product 102
2024-01-15 11:20:30 INFO User bob@example.com added item 102 to cart
2024-01-15 11:21:15 INFO Order 12346 created for user bob@example.com
2024-01-15 12:00:00 INFO Daily backup completed successfully
2024-01-15 12:30:00 WARN High memory usage detected: 87%"""

        text_path = os.path.join(output_directory, "application.log")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(log_content)

        files_created.append({"file": "application.log", "type": "TEXT", "path": text_path})

        # 4. Sample TSV file (Tab-separated values)
        tsv_data = [
            {
                "product_id": "P001",
                "category": "Electronics",
                "sales_q1": "15000",
                "sales_q2": "18000",
                "sales_q3": "22000",
                "sales_q4": "25000",
            },
            {
                "product_id": "P002",
                "category": "Books",
                "sales_q1": "8000",
                "sales_q2": "7500",
                "sales_q3": "9000",
                "sales_q4": "12000",
            },
            {
                "product_id": "P003",
                "category": "Electronics",
                "sales_q1": "12000",
                "sales_q2": "14000",
                "sales_q3": "16000",
                "sales_q4": "19000",
            },
            {
                "product_id": "P004",
                "category": "Home",
                "sales_q1": "5000",
                "sales_q2": "6000",
                "sales_q3": "7500",
                "sales_q4": "9000",
            },
        ]

        tsv_path = os.path.join(output_directory, "sales_data.tsv")
        tsv_result = write_csv_file(tsv_path, tsv_data, delimiter="\t")
        if "error" not in tsv_result:
            files_created.append({"file": "sales_data.tsv", "type": "TSV", "path": tsv_path})

        result = {
            "status": "success",
            "output_directory": output_directory,
            "files_created": files_created,
            "total_files": len(files_created),
            "description": "Sample files created for testing file processing tools",
        }

        logger.info(f"Created {len(files_created)} sample files in {output_directory}")
        return result

    except Exception as e:
        logger.error(f"Error creating sample files: {str(e)}")
        return {"error": f"Failed to create sample files: {str(e)}"}
