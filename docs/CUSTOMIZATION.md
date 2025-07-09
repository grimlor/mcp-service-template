# Template Customization Guide

This guide walks you through customizing the MCP Service Template for your specific use case.

## 🎯 Quick Start Checklist

Follow this checklist to customize the template:

### 1. **Basic Setup** ✅
- [ ] Clone/copy the template to your new project directory
- [ ] Replace all `{{service_name}}` placeholders with your actual service name
- [ ] Replace all `{{Service Name}}` placeholders with your display name
- [ ] Replace all `{{Domain}}` placeholders with your business domain
- [ ] Update `pyproject.toml` with your service details

### 2. **Directory Structure** ✅
- [ ] Rename `src/service_name_mcp/` to `src/your_service_mcp/`
- [ ] Update import statements throughout the codebase
- [ ] Remove example domains you don't need
- [ ] Add your specific domain modules

### 3. **Configuration** ⚙️
- [ ] Update `src/your_service_mcp/common/config.py` with your settings
- [ ] Configure authentication and connection settings
- [ ] Set up environment variables for your deployment
- [ ] Update logging configuration if needed

### 4. **Tool Implementation** 🔧
- [ ] Implement your domain-specific tools in each domain module
- [ ] Replace mock functions with real implementations
- [ ] Update tool descriptions and parameters
- [ ] Add your business-specific validation logic

### 5. **Prompts and Documentation** 📚
- [ ] Customize prompts in `src/your_service_mcp/core/prompts/`
- [ ] Update best practices files for each domain
- [ ] Add your domain-specific documentation
- [ ] Update the main README.md

### 6. **Testing** 🧪
- [ ] Update tests with your service-specific logic
- [ ] Add integration tests for your data sources
- [ ] Create test data and fixtures
- [ ] Set up continuous integration

### 7. **Deployment** 🚀
- [ ] Configure your deployment environment
- [ ] Set up authentication and permissions
- [ ] Test end-to-end functionality
- [ ] Deploy to your target environment

## 📝 Detailed Customization Steps

### Step 1: Project Naming and Structure

1. **Rename the main package directory**:
   ```bash
   mv src/service_name_mcp src/your_service_mcp
   ```

2. **Update pyproject.toml**:
   ```toml
   [project]
   name = "your-service-mcp"
   description = "Your Service Description MCP Server"
   
   [project.scripts]
   your-service-mcp = "your_service_mcp.server:main"
   ```

3. **Find and replace placeholders**:
   - `{{service_name}}` → `your_service`
   - `{{Service Name}}` → `Your Service Name`
   - `{{Domain}}` → `Your Domain`
   - `{{domain}}` → `your domain`

### Step 2: Update Imports

Update all import statements throughout the codebase:

```python
# Before
from service_name_mcp.mcp_instance import mcp

# After  
from your_service_mcp.mcp_instance import mcp
```

### Step 3: Configure Your Service

Update `src/your_service_mcp/mcp_instance.py`:

```python
mcp = FastMCP(
    title="your-service-mcp-server", 
    instructions="Your Service MCP server providing AI agents with access to your domain data and functionality"
)
```

### Step 4: Implement Domain Tools

Choose which domain modules you need:

#### Keep and Customize:
- **Kusto Domain**: If you use Azure Data Explorer/Kusto
- **Semantic Model Domain**: If you use Power BI/Analysis Services
- **Docs Domain**: If you have searchable documentation
- **Analytics Domain**: If you need advanced analytics

#### Remove Unused Domains:
```bash
rm -rf src/your_service_mcp/unused_domain/
```

#### Update server.py imports:
```python
# Remove unused imports
# import your_service_mcp.unused_domain.tools

# Keep needed imports
import your_service_mcp.kusto_domain.kusto_tools
import your_service_mcp.core.core_prompts
# ... other needed imports
```

### Step 5: Implement Real Functionality

Replace template mock functions with real implementations:

#### Example: Kusto Tools
```python
# Replace this template code:
def _execute(query: str, database: Optional[str] = None):
    return [{"message": "Query execution not implemented - this is a template"}]

# With real implementation:
def _execute(query: str, database: Optional[str] = None):
    client = get_kusto_query_client(KUSTO_CLUSTER_URI)
    crp = ClientRequestProperties()
    result_set = client.execute(database, query, crp)
    return format_results(result_set)
```

#### Example: Documentation Tools
```python
# Replace mock search with real implementation:
def search_documentation(search_text: str, path_filter: Optional[str] = None):
    # Implement real search using your documentation platform
    # Azure DevOps, SharePoint, Elasticsearch, etc.
    client = YourDocumentationClient()
    return client.search(search_text, path_filter)
```

### Step 6: Configure Authentication

Set up authentication for your data sources:

#### Azure Services:
```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
```

#### Custom Authentication:
```python
class CustomAuthenticator:
    def __init__(self):
        self.token = os.getenv("API_TOKEN")
    
    def get_headers(self):
        return {"Authorization": f"Bearer {self.token}"}
```

### Step 7: Update Configuration

Customize `src/your_service_mcp/common/config.py`:

```python
class Config:
    # Your service-specific configuration
    SERVICE_NAME = os.getenv("SERVICE_NAME", "your_service")
    
    # Data source configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    API_ENDPOINT = os.getenv("API_ENDPOINT", "")
    
    # Authentication
    CLIENT_ID = os.getenv("CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
    
    # Feature flags
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"
```

### Step 8: Customize Prompts

Update prompts in `src/your_service_mcp/core/prompts/`:

#### analyst_prompt.md:
```markdown
# Expert Your Domain Data Analyst

You are an expert in analyzing your domain data using the Your Service platform.

## Your Expertise:
- Deep knowledge of your domain processes
- Expert in your domain query languages and tools
- Understanding of your domain metrics and KPIs

## Key Principles:
1. Always validate data quality
2. Provide query traceability
3. Focus on actionable insights
```

### Step 9: Add Domain-Specific Logic

Implement your business-specific logic:

#### Custom Metrics:
```python
def calculate_your_domain_metric(data, parameters):
    # Implement your domain-specific metric calculation
    return result

def validate_your_domain_data(data):
    # Implement your data validation logic
    return is_valid, error_message
```

#### Custom Analysis:
```python
@mcp.tool(description="Your domain-specific analysis")
def your_domain_analysis(parameters):
    # Implement your specialized analysis
    return results
```

### Step 10: Testing and Validation

Create comprehensive tests:

> **Note**: For setting up `uv` and installing dependencies, see the detailed instructions in [SETUP.md](SETUP.md).

#### Unit Tests:
```python
def test_your_domain_tool():
    # Test your domain-specific functionality
    result = your_domain_tool(test_parameters)
    assert result["status"] == "success"
```

#### Integration Tests:
```python
def test_end_to_end_workflow():
    # Test complete workflows
    # Authenticate → Query → Analyze → Return results
    pass
```

#### Run Tests:
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/your_service_mcp --cov-report=html

# Run specific tests
uv run pytest tests/test_your_domain/
```

### Step 11: Documentation

Update documentation:

1. **README.md**: Describe your service and capabilities
2. **Best Practices**: Create domain-specific best practices
3. **API Documentation**: Document your tools and their parameters
4. **Examples**: Provide usage examples and tutorials

### Step 12: Deployment

Prepare for deployment:

1. **Environment Configuration**: Set up production environment variables
2. **Dependencies**: Install required packages and services
3. **Authentication**: Configure production authentication
4. **Monitoring**: Set up logging and monitoring
5. **Testing**: Validate in production environment

## 🔧 Advanced Customizations

### Custom Tool Categories

Create new tool categories for your domain:

```python
# src/your_service_mcp/your_domain/
├── __init__.py
├── your_domain_tools.py      # Main tools
├── your_domain_config.py     # Configuration
├── your_domain_prompts.py    # Domain prompts
└── your_domain_utils.py      # Utilities
```

### Custom Response Formats

Implement custom result formatting:

```python
def format_your_domain_results(data):
    return {
        "summary": create_summary(data),
        "details": format_details(data),
        "visualizations": generate_charts(data),
        "recommendations": generate_recommendations(data)
    }
```

### Performance Optimization

Optimize for your specific use case:

```python
# Caching
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_expensive_operation(parameters):
    return expensive_operation(parameters)

# Connection pooling
class ConnectionPool:
    def __init__(self, max_connections=10):
        self.pool = create_connection_pool(max_connections)
```

## 🚨 Common Pitfalls

### 1. **Import Errors**
- Ensure all imports are updated after renaming packages
- Check that all modules are properly installed

### 2. **Configuration Issues**
- Validate all required environment variables are set
- Test authentication in your target environment

### 3. **Tool Registration**
- Ensure all tool modules are imported in `server.py`
- Verify tool descriptions are clear and accurate

### 4. **Performance Problems**
- Test with realistic data volumes
- Implement appropriate caching and connection management
- Monitor query performance and resource usage

## 🔄 Iterative Development

1. **Start Simple**: Begin with basic functionality and expand
2. **Test Early**: Validate each component as you build it
3. **Get Feedback**: Test with real users and use cases
4. **Iterate**: Continuously improve based on usage patterns

## 📞 Getting Help

- Check the template documentation for examples
- Review the original PDP implementation for patterns
- Test individual components in isolation
- Use logging and debugging tools effectively

---

This customization guide provides a systematic approach to adapting the MCP Service Template for your specific needs. Take it step by step, and don't hesitate to adapt the patterns to match your domain requirements.
