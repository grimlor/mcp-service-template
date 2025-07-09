# REST API Domain Best Practices

## Overview
The REST API domain demonstrates HTTP client integration patterns using free, public APIs that require no authentication or setup. This domain teaches API integration fundamentals that apply to any REST API.

## Key Learning Objectives

### 1. **HTTP Client Management**
- Session reuse and connection pooling
- Proper header management and user agent setting
- Timeout configuration and resource cleanup

### 2. **Request/Response Handling**
- Different HTTP methods (GET, POST, PUT, DELETE)
- Query parameters and request body handling
- Response parsing (JSON, text, binary)
- Status code interpretation and error handling

### 3. **Error Handling and Resilience**
- Network timeout and connectivity errors
- HTTP error status codes (4xx, 5xx)
- JSON parsing errors and content type handling
- Graceful degradation when APIs are unavailable

### 4. **Data Transformation**
- Response data extraction and formatting
- Metadata collection and enrichment
- Result standardization across different APIs

## Free APIs Used

### 1. **Weather Data**
- **API**: wttr.in
- **Purpose**: Weather information without API keys
- **Learning**: Location-based queries, data formatting

### 2. **Random Content**
- **APIs**: quotable.io, uselessfacts.jsph.pl, official-joke-api, adviceslip.com
- **Purpose**: Content APIs with different response structures
- **Learning**: Multiple API integration, content type handling

### 3. **Country Information**
- **API**: restcountries.com
- **Purpose**: Geographic and political data
- **Learning**: Complex data structures, search patterns

### 4. **Test Data**
- **API**: jsonplaceholder.typicode.com
- **Purpose**: Fake REST API for testing
- **Learning**: CRUD operations, resource relationships

## Tool Usage Examples

### Weather Data
```python
# Get weather for a city
weather = get_weather_data("London", "GB", "metric")

# Check for errors
if "error" not in weather:
    temp = weather["current"]["temperature"]
    desc = weather["current"]["description"]
    print(f"Temperature: {temp}°C, {desc}")
```

### Random Content
```python
# Get different types of content
quote = get_random_content("quote")
fact = get_random_content("fact")
joke = get_random_content("joke")
advice = get_random_content("advice")
```

### Country Information
```python
# Get basic country info
basic = get_country_info("Japan", "basic")

# Get detailed information
detailed = get_country_info("JP", "detailed")

# Get currency information
currency = get_country_info("United States", "currency")
```

### Custom Requests
```python
# Make custom API calls
response = make_http_request(
    "https://api.github.com/users/octocat",
    method="GET",
    headers={"Accept": "application/vnd.github.v3+json"}
)
```

## Best Practices

### 1. **Session Management**
```python
# Always reuse sessions for better performance
session = requests.Session()
session.headers.update({"User-Agent": "YourApp/1.0"})

# Set reasonable timeouts
session.timeout = 30
```

### 2. **Error Handling**
```python
try:
    response = session.get(url, timeout=10)
    response.raise_for_status()  # Raises exception for HTTP errors
    data = response.json()
except requests.exceptions.Timeout:
    # Handle timeout specifically
    return {"error": "Request timed out"}
except requests.exceptions.RequestException as e:
    # Handle other request errors
    return {"error": f"Request failed: {str(e)}"}
except ValueError as e:
    # Handle JSON parsing errors
    return {"error": f"Invalid JSON response: {str(e)}"}
```

### 3. **Response Validation**
```python
def validate_response(response):
    if not response.ok:
        return False, f"HTTP {response.status_code}: {response.reason}"
    
    content_type = response.headers.get('content-type', '')
    if 'application/json' not in content_type:
        return False, "Expected JSON response"
    
    return True, None
```

### 4. **Rate Limiting**
```python
import time
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, calls_per_minute=60):
        self.calls_per_minute = calls_per_minute
        self.calls = []
    
    def wait_if_needed(self):
        now = datetime.now()
        # Remove calls older than 1 minute
        self.calls = [call for call in self.calls if now - call < timedelta(minutes=1)]
        
        if len(self.calls) >= self.calls_per_minute:
            sleep_time = 60 - (now - self.calls[0]).total_seconds()
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.calls.append(now)
```

## Security Considerations

### 1. **Input Validation**
- Validate URLs to prevent SSRF attacks
- Sanitize user inputs used in API calls
- Restrict allowed domains/endpoints

### 2. **Credential Management**
- Never hardcode API keys in source code
- Use environment variables for sensitive data
- Implement proper authentication flows

### 3. **Data Privacy**
- Don't log sensitive request/response data
- Mask or redact personal information
- Respect API terms of service

## Performance Optimization

### 1. **Connection Pooling**
```python
# Use session for connection reuse
session = requests.Session()

# Configure connection pooling
adapter = requests.adapters.HTTPAdapter(
    pool_connections=10,
    pool_maxsize=20,
    max_retries=3
)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

### 2. **Caching**
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=128)
def cached_api_call(url, params_hash):
    # Implementation here
    pass

def make_cached_request(url, params):
    params_hash = hashlib.md5(str(sorted(params.items())).encode()).hexdigest()
    return cached_api_call(url, params_hash)
```

### 3. **Async Operations**
```python
import asyncio
import aiohttp

async def fetch_multiple_apis(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch_url(session, url))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.json()
```

## Testing and Development

### 1. **Mock API Responses**
```python
import responses

@responses.activate
def test_api_integration():
    responses.add(
        responses.GET,
        'https://api.example.com/data',
        json={'key': 'value'},
        status=200
    )
    
    result = make_api_call('https://api.example.com/data')
    assert result['key'] == 'value'
```

### 2. **Integration Testing**
```python
def test_real_api_integration():
    # Test with actual API (use sparingly)
    result = get_weather_data("London")
    
    assert "error" not in result
    assert "current" in result
    assert "temperature" in result["current"]
```

### 3. **Error Simulation**
```python
def test_network_errors():
    # Test timeout handling
    with patch('requests.Session.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout()
        
        result = get_weather_data("London")
        assert "error" in result
        assert "timeout" in result["error"].lower()
```

## Common Patterns

### 1. **API Client Class**
```python
class APIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        return self.session.get(url, params=params)
    
    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        return self.session.post(url, json=data)
```

### 2. **Response Wrapper**
```python
class APIResponse:
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        
    @property
    def is_success(self):
        return self.response.ok
    
    @property
    def data(self):
        try:
            return self.response.json()
        except ValueError:
            return self.response.text
    
    @property
    def error_message(self):
        if self.is_success:
            return None
        return f"HTTP {self.status_code}: {self.response.reason}"
```

### 3. **Retry Logic**
```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator
```

## Learning Exercises

### 1. **Basic API Calls**
1. Use each tool to explore different response structures
2. Practice error handling with invalid inputs
3. Understand different content types and parsing

### 2. **Data Processing**
1. Extract specific fields from API responses
2. Combine data from multiple API calls
3. Format responses for different use cases

### 3. **Error Scenarios**
1. Test network timeouts and connectivity issues
2. Handle HTTP error status codes
3. Deal with malformed or unexpected responses

### 4. **Performance Testing**
1. Measure API response times
2. Test concurrent requests
3. Implement caching strategies

This REST API domain provides comprehensive patterns for HTTP client integration that can be applied to any REST API, while using only free, publicly available services for learning.
