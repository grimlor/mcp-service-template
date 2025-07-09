# File Processing Domain Best Practices

## Overview
The File Processing domain demonstrates file I/O patterns for common data formats (CSV, JSON, text) using only standard Python libraries. This domain teaches essential file handling skills applicable to any data processing scenario.

## Key Learning Objectives

### 1. **File I/O Operations**
- Safe file reading with proper error handling
- File writing with directory creation
- Encoding handling for international content
- File size validation and memory management

### 2. **CSV Processing**
- Dialect detection and delimiter handling
- Header processing and data type inference
- Large file handling with row limits
- Data validation and cleaning

### 3. **JSON Manipulation**
- JSON parsing and structure analysis
- Complex nested object handling
- Data type preservation and conversion
- Memory-efficient processing

### 4. **Text Analysis**
- Character and word frequency analysis
- Content pattern recognition
- Statistical text analysis
- Sample extraction for large files

## Tool Usage Examples

### CSV Operations
```python
# Read CSV with automatic analysis
result = read_csv_file(
    "data/customers.csv",
    delimiter=",",
    has_header=True,
    max_rows=1000
)

# Check for errors
if "error" not in result:
    data = result["data"]
    analysis = result["column_analysis"]
    print(f"Loaded {len(data)} rows with {result['structure']['column_count']} columns")

# Write processed data back to CSV
write_csv_file("output/processed_customers.csv", processed_data)
```

### JSON Processing
```python
# Read and analyze JSON structure
result = read_json_file("config/settings.json")

if "error" not in result:
    data = result["data"]
    structure = result["analysis"]["structure"]
    depth = result["analysis"]["size_estimate"]["depth"]
    
    print(f"JSON depth: {depth}")

# Write complex data structures
write_json_file("output/results.json", complex_data, indent=2)
```

### Text Analysis
```python
# Analyze log files
analysis = analyze_text_file(
    "logs/application.log",
    encoding="utf-8",
    max_lines=10000
)

if "error" not in analysis:
    stats = analysis["statistics"]
    common_words = analysis["content_analysis"]["common_words"]
    
    print(f"Total lines: {stats['total_lines']}")
    print(f"Most common words: {common_words[:5]}")
```

### Directory Operations
```python
# List all CSV files recursively
files = list_directory_files(
    "data/",
    pattern="*.csv",
    include_subdirs=True,
    file_types=[".csv", ".tsv"]
)

for file_info in files["files"]:
    print(f"{file_info['name']}: {file_info['size_bytes']} bytes")
```

## Best Practices

### 1. **File Safety**
```python
# Always check if file exists
if not os.path.exists(file_path):
    return {"error": f"File not found: {file_path}"}

# Validate file size before processing
file_size = os.path.getsize(file_path)
if file_size > MAX_FILE_SIZE:
    return {"error": f"File too large: {file_size} bytes"}

# Use context managers for file operations
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
```

### 2. **Encoding Handling**
```python
# Always specify encoding explicitly
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Handle encoding errors gracefully
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    # Try alternative encodings
    for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
```

### 3. **Memory Management**
```python
# Process large files in chunks
def process_large_csv(file_path, chunk_size=1000):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        chunk = []
        
        for row in reader:
            chunk.append(row)
            
            if len(chunk) >= chunk_size:
                process_chunk(chunk)
                chunk = []
        
        # Process remaining rows
        if chunk:
            process_chunk(chunk)

# Use generators for memory efficiency
def read_lines_generator(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()
```

### 4. **Error Handling**
```python
# Comprehensive error handling
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    return {"error": f"File not found: {file_path}"}
except PermissionError:
    return {"error": f"Permission denied: {file_path}"}
except json.JSONDecodeError as e:
    return {"error": f"Invalid JSON: {str(e)}"}
except UnicodeDecodeError as e:
    return {"error": f"Encoding error: {str(e)}"}
except Exception as e:
    return {"error": f"Unexpected error: {str(e)}"}
```

## Performance Considerations

### 1. **Large File Handling**
```python
# Read files in chunks
def read_large_file_chunks(file_path, chunk_size=8192):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Limit processing for very large files
MAX_ROWS = 100000
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

if row_count > MAX_ROWS:
    logger.warning(f"File too large, processing first {MAX_ROWS} rows only")
```

### 2. **Efficient Data Structures**
```python
# Use appropriate data structures
from collections import defaultdict, Counter

# For frequency counting
word_freq = Counter()
for line in lines:
    words = line.split()
    word_freq.update(words)

# For grouping data
grouped_data = defaultdict(list)
for row in csv_data:
    category = row['category']
    grouped_data[category].append(row)
```

### 3. **Streaming Processing**
```python
# Process JSON streams
import ijson

def process_json_stream(file_path):
    with open(file_path, 'rb') as f:
        # Parse specific parts of large JSON
        items = ijson.items(f, 'data.items.item')
        for item in items:
            process_item(item)
```

## Security Considerations

### 1. **Path Validation**
```python
import os.path

def validate_file_path(file_path, allowed_dirs):
    # Resolve to absolute path
    abs_path = os.path.abspath(file_path)
    
    # Check if within allowed directories
    for allowed_dir in allowed_dirs:
        if abs_path.startswith(os.path.abspath(allowed_dir)):
            return True
    
    return False

# Prevent directory traversal
if '../' in file_path or '..\\' in file_path:
    return {"error": "Invalid file path"}
```

### 2. **Content Validation**
```python
# Validate CSV headers
EXPECTED_HEADERS = ['id', 'name', 'email', 'age']

def validate_csv_headers(headers):
    if not all(header in EXPECTED_HEADERS for header in headers):
        return False, "Invalid headers"
    return True, None

# Sanitize file content
def sanitize_text_content(content):
    # Remove potential script tags or dangerous content
    import re
    clean_content = re.sub(r'<script.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
    return clean_content
```

### 3. **Resource Limits**
```python
# Implement timeouts for file operations
import signal

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("File operation timed out")

# Set timeout for file operations
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 second timeout

try:
    # File operation here
    process_file(file_path)
finally:
    signal.alarm(0)  # Cancel timeout
```

## Data Quality and Validation

### 1. **CSV Data Validation**
```python
def validate_csv_row(row, schema):
    errors = []
    
    for field, rules in schema.items():
        value = row.get(field, '')
        
        # Required field check
        if rules.get('required') and not value:
            errors.append(f"Missing required field: {field}")
        
        # Data type validation
        if value and 'type' in rules:
            if rules['type'] == 'int':
                try:
                    int(value)
                except ValueError:
                    errors.append(f"Invalid integer: {field}")
            elif rules['type'] == 'email':
                if '@' not in value:
                    errors.append(f"Invalid email: {field}")
    
    return errors

# Schema example
CUSTOMER_SCHEMA = {
    'customer_id': {'required': True, 'type': 'int'},
    'email': {'required': True, 'type': 'email'},
    'age': {'required': False, 'type': 'int'}
}
```

### 2. **Data Type Inference**
```python
def infer_column_type(values):
    """Infer the most likely data type for a column"""
    if not values:
        return 'unknown'
    
    # Sample some values for analysis
    sample = values[:100]
    
    # Check for integers
    int_count = 0
    float_count = 0
    date_count = 0
    
    for value in sample:
        if not value.strip():
            continue
            
        try:
            int(value)
            int_count += 1
        except ValueError:
            try:
                float(value)
                float_count += 1
            except ValueError:
                # Check for dates
                if re.match(r'\d{4}-\d{2}-\d{2}', value):
                    date_count += 1
    
    total = len([v for v in sample if v.strip()])
    
    if int_count / total > 0.8:
        return 'integer'
    elif float_count / total > 0.8:
        return 'float'
    elif date_count / total > 0.8:
        return 'date'
    else:
        return 'string'
```

## Advanced Patterns

### 1. **File Format Detection**
```python
def detect_file_format(file_path):
    """Detect file format based on content"""
    with open(file_path, 'rb') as f:
        header = f.read(1024)
    
    # Check for BOM
    if header.startswith(b'\xef\xbb\xbf'):
        encoding = 'utf-8-sig'
    elif header.startswith(b'\xff\xfe'):
        encoding = 'utf-16-le'
    else:
        encoding = 'utf-8'
    
    # Try to detect CSV vs JSON vs text
    try:
        header_text = header.decode(encoding)
        
        if header_text.strip().startswith(('{', '[')):
            return 'json', encoding
        elif ',' in header_text and '\n' in header_text:
            return 'csv', encoding
        else:
            return 'text', encoding
    except UnicodeDecodeError:
        return 'binary', None
```

### 2. **Data Transformation Pipelines**
```python
class FileProcessor:
    def __init__(self):
        self.transformations = []
    
    def add_transformation(self, func):
        self.transformations.append(func)
        return self
    
    def process(self, data):
        result = data
        for transform in self.transformations:
            result = transform(result)
        return result

# Usage
processor = FileProcessor()
processor.add_transformation(clean_whitespace)
processor.add_transformation(validate_emails)
processor.add_transformation(normalize_dates)

processed_data = processor.process(raw_data)
```

### 3. **Batch File Processing**
```python
def process_file_batch(file_paths, processor_func, parallel=False):
    """Process multiple files with optional parallelization"""
    results = []
    
    if parallel:
        from concurrent.futures import ThreadPoolExecutor
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {
                executor.submit(processor_func, file_path): file_path 
                for file_path in file_paths
            }
            
            for future in future_to_file:
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append({"file": file_path, "result": result})
                except Exception as e:
                    results.append({"file": file_path, "error": str(e)})
    else:
        for file_path in file_paths:
            try:
                result = processor_func(file_path)
                results.append({"file": file_path, "result": result})
            except Exception as e:
                results.append({"file": file_path, "error": str(e)})
    
    return results
```

## Learning Exercises

### 1. **Basic File Operations**
1. Create sample files using the provided tool
2. Read different file formats (CSV, JSON, text)
3. Practice error handling with invalid files
4. Experiment with different encodings

### 2. **Data Analysis**
1. Analyze CSV files with different delimiters
2. Explore JSON structure analysis
3. Perform text analysis on log files
4. Compare file sizes and processing times

### 3. **Data Transformation**
1. Convert between CSV and JSON formats
2. Clean and validate data during processing
3. Merge data from multiple files
4. Create data processing pipelines

### 4. **Performance Testing**
1. Test with large files (create using tools)
2. Measure memory usage during processing
3. Compare different processing strategies
4. Implement streaming for large datasets

This File Processing domain provides essential patterns for handling common data formats that can be applied to any file-based data processing scenario, using only standard libraries available everywhere.
