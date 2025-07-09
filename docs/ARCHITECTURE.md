# Architecture Guide

This guide explains the key architectural patterns and design principles used in the MCP Service Template.

## 🏗️ Core Architecture Principles

### 1. **Modular Domain Organization**
Each business domain has its own module with standardized structure:

```
your_domain/
├── __init__.py
├── domain_tools.py         # MCP tool implementations
├── domain_config.py        # Domain-specific configuration (optional)
├── domain_prompts.py       # Domain-specific prompts (optional)
├── domain_utils.py         # Utility functions (optional)
└── best_practices.md       # Documentation and patterns
```

### 2. **Centralized MCP Instance**
Single FastMCP instance shared across all domains:

```python
# mcp_instance.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    title="your-service-mcp-server",
    instructions="Your service description and capabilities"
)
```

### 3. **Tool Registration Pattern**
Consistent tool registration across all domains:

```python
# In any domain_tools.py
from your_service_mcp.mcp_instance import mcp

@mcp.tool(description="Clear, concise tool description")
def your_tool_name(
    param1: str,
    param2: Optional[int] = None
) -> Dict[str, Any]:
    """
    Detailed docstring explaining:
    - Purpose and functionality
    - Parameter meanings and constraints
    - Return value structure
    - Usage examples
    """
    try:
        # Your implementation here
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error in your_tool_name: {str(e)}")
        return {"status": "error", "message": str(e)}
```

### 4. **Prompt System Pattern**
Structured prompt system with file-based templates:

```python
# core_prompts.py
from mcp.server.models import base
from pathlib import Path

def _load_prompt_content(filename: str) -> str:
    """Load prompt content from markdown files"""
    prompt_path = Path(__file__).parent / "prompts" / filename
    return prompt_path.read_text(encoding="utf-8")

@mcp.prompt()
def domain_expert() -> list[base.Message]:
    """Expert prompt for domain analysis"""
    return [
        base.UserMessage(_load_prompt_content("analyst_prompt.md")),
        base.AssistantMessage("Ready to assist with domain analysis!")
    ]
```

### 5. **Configuration Management Pattern**
Environment-based configuration with validation:

```python
# common/config.py
import os
from typing import Optional, Tuple

class Config:
    # Service Configuration
    SERVICE_NAME = os.getenv("SERVICE_NAME", "your_service")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # External Service Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    API_ENDPOINT = os.getenv("API_ENDPOINT", "")
    API_KEY = os.getenv("API_KEY", "")

    # Feature Flags
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "300"))

    @classmethod
    def validate(cls) -> Tuple[bool, Optional[str]]:
        """Validate required configuration"""
        required_vars = ["DATABASE_URL", "API_KEY"]

        for var in required_vars:
            if not getattr(cls, var):
                return False, f"Missing required configuration: {var}"

        return True, None
```

### 6. **Logging Pattern**
Structured logging with correlation IDs:

```python
# common/logging.py
import logging
import uuid
from contextlib import contextmanager

def setup_logging(level: str = "INFO"):
    """Setup structured logging"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(correlation_id)s - %(message)s'
    )

def get_logger(name: str) -> logging.Logger:
    """Get logger with correlation ID support"""
    return logging.getLogger(name)

@contextmanager
def correlation_context(correlation_id: str = None):
    """Add correlation ID to log context"""
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())[:8]

    # Implementation depends on your logging framework
    # This is a simplified example
    yield correlation_id
```

## 🔧 Design Patterns

### 1. **Repository Pattern for Data Access**
```python
# domain/domain_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class DomainRepository(ABC):
    """Abstract repository for domain data access"""

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def search(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> str:
        pass

class DatabaseDomainRepository(DomainRepository):
    """Concrete implementation using database"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        # Database implementation
        pass
```

### 2. **Service Layer Pattern**
```python
# domain/domain_service.py
from typing import Dict, Any, List
from .domain_repository import DomainRepository

class DomainService:
    """Business logic layer for domain operations"""

    def __init__(self, repository: DomainRepository):
        self.repository = repository

    def analyze_data(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """High-level business operation"""
        # Validation
        if not self._validate_criteria(criteria):
            raise ValueError("Invalid criteria")

        # Business logic
        raw_data = self.repository.search(criteria)
        processed_data = self._process_data(raw_data)
        insights = self._generate_insights(processed_data)

        return {
            "data": processed_data,
            "insights": insights,
            "metadata": self._get_metadata(criteria)
        }

    def _validate_criteria(self, criteria: Dict[str, Any]) -> bool:
        # Validation logic
        return True

    def _process_data(self, data: List[Dict]) -> List[Dict]:
        # Data processing logic
        return data

    def _generate_insights(self, data: List[Dict]) -> Dict[str, Any]:
        # Insight generation logic
        return {}

    def _get_metadata(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        # Metadata generation
        return {"timestamp": "2024-01-01T00:00:00Z"}
```

### 3. **Factory Pattern for Tool Creation**
```python
# domain/domain_factory.py
from .domain_service import DomainService
from .domain_repository import DatabaseDomainRepository
from ..common.config import Config

class DomainFactory:
    """Factory for creating domain objects"""

    @staticmethod
    def create_service() -> DomainService:
        """Create configured domain service"""
        repository = DatabaseDomainRepository(Config.DATABASE_URL)
        return DomainService(repository)

    @staticmethod
    def create_repository() -> DomainRepository:
        """Create configured repository"""
        return DatabaseDomainRepository(Config.DATABASE_URL)
```

### 4. **Error Handling Pattern**
```python
# common/exceptions.py
class ServiceException(Exception):
    """Base exception for service errors"""
    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.error_code = error_code

class ValidationError(ServiceException):
    """Validation error"""
    pass

class DataAccessError(ServiceException):
    """Data access error"""
    pass

class ExternalServiceError(ServiceException):
    """External service error"""
    pass

# In tool implementations
def handle_service_errors(func):
    """Decorator for consistent error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return {"status": "error", "type": "validation", "message": str(e)}
        except DataAccessError as e:
            return {"status": "error", "type": "data_access", "message": str(e)}
        except ExternalServiceError as e:
            return {"status": "error", "type": "external_service", "message": str(e)}
        except Exception as e:
            logger.exception(f"Unexpected error in {func.__name__}")
            return {"status": "error", "type": "internal", "message": "Internal server error"}
    return wrapper
```

## 🚀 Performance Patterns

### 1. **Caching Pattern**
```python
# common/cache.py
from functools import wraps
import time
from typing import Dict, Any, Callable

class SimpleCache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds

    def get(self, key: str) -> Any:
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry["timestamp"] < self.ttl_seconds:
                return entry["value"]
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any):
        self.cache[key] = {
            "value": value,
            "timestamp": time.time()
        }

def cached(ttl_seconds: int = 300):
    """Caching decorator"""
    cache = SimpleCache(ttl_seconds)

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute and cache
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            return result

        return wrapper
    return decorator
```

### 2. **Connection Pooling Pattern**
```python
# common/connections.py
from contextlib import contextmanager
import queue
import threading
from typing import Any, Iterator

class ConnectionPool:
    def __init__(self, create_connection: Callable, max_connections: int = 10):
        self.create_connection = create_connection
        self.pool = queue.Queue(maxsize=max_connections)
        self.lock = threading.Lock()

        # Pre-populate pool
        for _ in range(max_connections):
            self.pool.put(self.create_connection())

    @contextmanager
    def get_connection(self) -> Iterator[Any]:
        connection = self.pool.get()
        try:
            yield connection
        finally:
            self.pool.put(connection)
```

## 📋 Best Practices

### 1. **Tool Design Guidelines**
- **Single Responsibility**: Each tool should do one thing well
- **Clear Parameters**: Use type hints and clear parameter names
- **Comprehensive Documentation**: Include docstrings with examples
- **Error Handling**: Return structured error responses
- **Input Validation**: Validate all parameters
- **Output Consistency**: Use consistent response formats

### 2. **Configuration Guidelines**
- **Environment Variables**: Use environment variables for configuration
- **Validation**: Validate configuration at startup
- **Defaults**: Provide sensible defaults
- **Documentation**: Document all configuration options
- **Secrets**: Never hardcode secrets

### 3. **Testing Guidelines**
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test interactions between components
- **Mocking**: Mock external dependencies
- **Coverage**: Aim for high test coverage
- **Test Data**: Use realistic test data

### 4. **Performance Guidelines**
- **Caching**: Cache expensive operations
- **Connection Pooling**: Pool database connections
- **Async Operations**: Use async/await for I/O operations
- **Pagination**: Implement pagination for large datasets
- **Monitoring**: Monitor performance metrics

This architecture guide provides the foundation for building robust, maintainable MCP services. Follow these patterns consistently across all domains for the best results.
