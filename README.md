# MCP Service Template

A template for creating Model Context Protocol (MCP) servers that provide AI agents with access to domain-specific data and functionality. This template is based on proven patterns from production MCP services and provides a solid foundation for building new MCP-enabled services.

## 🏗️ Template Overview

This template provides:
- **🔧 Core MCP Infrastructure** - Server setup, logging, and configuration
- **🔌 Tool Architecture** - Modular tool organization by domain
- **📊 Data Integration Patterns** - Examples for SQLite, REST APIs, and File Processing
- **🎯 Prompt System** - Domain-specific AI prompts and instructions
- **📚 Documentation Tools** - Searchable documentation integration
- **⚙️ Configuration Management** - Environment-based settings
- **🧪 Testing Framework** - Unit and integration testing setup
- **⚡ Modern Python Tooling** - `uv` for fast dependency management and `pyproject.toml` configuration

## 🚀 Getting Started

### 1. Quick Setup (Recommended)

The fastest way to get started is using our automated setup script:

```bash
python3 setup_template.py
```

**⚠️ Important**: Run the setup script first before using `uv` commands, as the template contains placeholders that need to be replaced.

This interactive script will:
- Prompt for your service details (name, description, domain)
- Replace all template placeholders automatically
- Rename directories and update imports
- Clean up template-specific files

**After setup, you'll have a fully customized MCP service ready for development!**

For detailed setup instructions, manual setup options, and troubleshooting, see [docs/SETUP.md](docs/SETUP.md).

### 2. Domain Examples Included

The template includes these domain examples to demonstrate patterns using free, widely available services:

- **`sqlite_domain/`** - Local SQLite database integration (no external services required)
- **`rest_api_domain/`** - HTTP client patterns with free public APIs
- **`file_processing_domain/`** - CSV, JSON, and text file processing
- **`docs_domain/`** - Documentation search and retrieval patterns
- **`analytics_domain/`** - Data science and analytics tools
- **`core/`** - Domain-agnostic prompts and utilities

### 3. Development Workflow

This template uses [`uv`](https://docs.astral.sh/uv/) for dependency management, which provides:
- ⚡ **10-100x faster** than pip
- 🔒 **Better dependency resolution** with automatic conflict detection  
- 📦 **Reproducible builds** with lock files
- 🛠️ **Integrated virtual environment** management

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and create virtual environment
uv sync --all-extras

# Run formatting and linting (configured in pyproject.toml)
uv run ruff format src/ tests/              # Code formatting
uv run ruff check src/ tests/               # Linting
uv run ruff check src/ tests/ --fix        # Auto-fix linting issues

# Run type checking
uv run mypy src/

# Run tests
uv run pytest

# Run the MCP server
uv run python3 -m {{service_name}}_mcp.server
```

### Automated Quality Checks (Git Hooks)

The template includes pre-commit hooks that automatically run quality checks before each commit:

```bash
# One-time setup: install the git hooks
uv run pre-commit install

# The hooks will now run automatically on git commit
# Or run manually on all files:
uv run pre-commit run --all-files
```

**What the hooks check:**
- 🎨 **Code formatting** with `ruff format`
- 🔍 **Linting** with `ruff check --fix`
- 🏷️ **Type checking** with `mypy`
- 📝 **File consistency** (trailing whitespace, line endings, etc.)

This ensures consistent code quality across all commits and prevents common issues from reaching your repository.

## 📁 Project Structure

```
mcp-service-template/
├── README.md                           # This file
├── pyproject.toml                      # Package configuration
├── MANIFEST.in                         # Include additional files in package
├── requirements.local.txt              # Local development dependencies
├── setup_template.py                   # Automated template setup script
├── validate_template.py                # Template validation script (maintainers only, auto-removed)
├── test_uv_compatibility.py           # uv compatibility validation
├── LICENSE                             # MIT License
├── src/
│   └── {{service_name}}_mcp/
│       ├── __init__.py                 # Package initialization and versioning
│       ├── server.py                   # Main MCP server entry point
│       ├── mcp_instance.py            # FastMCP server instance
│       ├── common/                     # Shared utilities
│       │   ├── __init__.py
│       │   ├── logging.py             # Logging configuration
│       │   └── config.py              # Environment configuration
│       ├── core/                       # Core prompts and utilities
│       │   ├── __init__.py
│       │   ├── core_prompts.py        # Domain-agnostic prompts
│       │   └── prompts/               # Prompt templates
│       │       ├── analyst_prompt.md
│       │       ├── report_bug_prompt.md
│       │       └── investigate_bug_prompt.md
│       ├── sqlite_domain/              # Example: Local SQLite database
│       │   ├── sqlite_tools.py        # SQL query tools
│       │   └── best_practices.md      # SQLite integration patterns
│       ├── rest_api_domain/           # Example: REST API integration
│       │   ├── rest_api_tools.py      # HTTP client tools
│       │   └── best_practices.md      # API integration patterns
│       ├── file_processing_domain/    # Example: File I/O operations
│       │   ├── file_processing_tools.py # CSV, JSON, text processing
│       │   └── best_practices.md      # File handling patterns
│       ├── docs_domain/               # Example: Documentation integration
│       │   ├── __init__.py
│       │   └── docs_tools.py          # Documentation search and retrieval
│       └── analytics_domain/          # Example: Analytics and data science
│           ├── __init__.py
│           ├── analytics_tools.py     # Data analysis and contribution tools
│           ├── analytics_prompts.py   # Analytics-specific prompts
│           └── README.md              # Analytics domain documentation
├── tests/                             # Test suite
│   ├── __init__.py
│   ├── test_server.py                 # Core server tests
│   ├── test_sqlite_domain/
│   │   ├── __init__.py
│   │   └── test_sqlite_tools.py       # SQLite domain tests
│   ├── test_rest_api_domain/
│   │   ├── __init__.py
│   │   └── test_rest_api_tools.py     # REST API domain tests
│   ├── test_file_processing_domain/
│   │   ├── __init__.py
│   │   └── test_file_processing_tools.py # File processing tests
│   ├── test_docs_domain/
│   │   ├── __init__.py
│   │   └── test_docs_tools.py         # Documentation domain tests
│   └── test_analytics_domain/
│       ├── __init__.py
│       └── test_analytics_tools.py    # Analytics domain tests
└── docs/                              # Documentation
    ├── SETUP.md                       # Detailed setup instructions
    ├── CUSTOMIZATION.md               # Template customization guide
    └── examples/
        └── ECOMMERCE_EXAMPLE.md       # E-commerce integration example
```

## 🔧 Key Architectural Patterns

### 1. **Modular Domain Organization**
Each business domain has its own module with:
- `*_tools.py` - MCP tool implementations
- `*_config.py` - Domain-specific configuration
- `*_prompts.py` - Domain-specific prompts (optional)
- `*.md` - Best practices and documentation

### 2. **Centralized MCP Instance**
```python
# mcp_instance.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    title="{{service_name}}-mcp-server", 
    instructions="{{Service Description}}"
)
```

### 3. **Tool Registration Pattern**
```python
# In tool modules
from {{service_name}}_mcp.mcp_instance import mcp

@mcp.tool(description="Tool description here")
def my_tool(param: str) -> str:
    """Tool implementation"""
    return result
```

### 4. **Prompt System Pattern**
```python
# core_prompts.py
@mcp.prompt()
def domain_expert() -> list[base.Message]:
    """Expert prompt for domain analysis"""
    return [
        base.UserMessage(_load_prompt_content("analyst_prompt.md")),
        base.AssistantMessage("Ready to assist!")
    ]
```

### 5. **Configuration Management**
```python
# common/config.py
import os

class Config:
    SERVICE_NAME = os.getenv("SERVICE_NAME", "{{service_name}}")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    # Add your configuration here
```

## 🔌 Available Tool Domains

### SQLite Domain (Example)
- Local database query execution
- Schema exploration and data sampling
- Best practices for SQL operations
- Connection management and transaction handling

### REST API Domain (Example)  
- HTTP client integration with public APIs
- Request/response handling and error management
- Authentication patterns and rate limiting
- Multiple API endpoint demonstrations

### File Processing Domain (Example)
- CSV, JSON, and text file processing
- File I/O operations and data transformation
- Directory traversal and batch processing
- Standard library-based implementations

### Documentation Domain (Example)
- Full-text search across documentation repositories
- Page content retrieval and caching
- Git repository and documentation platform integration
- Markdown content processing

### Analytics Domain (Example)
- Contribution analysis and performance attribution
- Statistical analysis and data science tools
- Query link generation for traceability
- Custom analysis frameworks

## 🎯 Prompt Engineering

The template includes sophisticated prompt patterns:

- **Role-based prompts** - Expert analyst personas
- **Context-aware instructions** - Domain-specific guidance
- **Tool integration** - Seamless tool usage instructions
- **Best practices** - Built-in quality guidelines
- **Error handling** - Graceful degradation patterns

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/{{service_name}}_mcp --cov-report=html

# Run specific domain tests
uv run pytest tests/test_sqlite_domain/

# Run integration tests
uv run pytest tests/integration/
```

## ✅ Template Validation

**For Template Maintainers & Contributors Only**

Use the validation script to ensure template integrity during development:

```bash
# Validate template structure and completeness
python3 validate_template.py
```

This script checks:
- Directory structure completeness
- Essential files presence  
- Domain module completeness
- Removal of platform-specific references
- Template placeholder presence

**Note**: This file is automatically removed when users run `setup_template.py`, as end users don't need template validation tools.

## 📦 Packaging & Distribution

```bash
# Build package
uv build

# Install locally in development mode
uv sync --all-extras

# Install with development dependencies
uv sync --all-extras

# Alternative: traditional pip install
pip install -e ".[dev]"
```

## 🔐 Security Considerations

- **Authentication** - Secure credential management and token handling
- **Authorization** - Role-based access control
- **Data Security** - No sensitive data in logs
- **Connection Security** - Secure credential management
- **Audit Logging** - Request tracking and monitoring

## 📚 Further Reading

- [Model Context Protocol Documentation](https://github.com/anthropics/mcp)
- [FastMCP Documentation](https://github.com/mcp-host/fastmcp) 
- [VS Code MCP Integration](https://docs.github.com/en/copilot)
- [Python Authentication Libraries](https://python-poetry.org/docs/repositories/#configuring-credentials)

## 🤝 Contributing

### For Template Contributors:

1. **Fork the template repository**
2. **Make your changes** to domains, documentation, or core functionality
3. **Validate your changes**:
   ```bash
   # Ensure template integrity (includes syntax checking)
   python3 validate_template.py
   
   # For faster syntax-only checking during development
   python3 validate_template.py --syntax-only
   ```
4. **Test the template works end-to-end**:
   ```bash
   # Copy template to test directory
   cp -r . /tmp/test-template
   cd /tmp/test-template
   
   # Run setup (use test values)
   python3 setup_template.py
   
   # Now uv should work on the instantiated template
   uv sync --all-extras
   uv run pytest
   ```
5. **Create your feature branch** (`git checkout -b feature/amazing-feature`)
6. **Commit your changes** (`git commit -m 'Add amazing feature'`)
7. **Push to the branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

**Note**: Template contributors can't run `uv run pytest` directly on the template because it contains placeholder names. Use the validation script and end-to-end testing instead.

### For Template Users:
- Report issues or suggest improvements via GitHub Issues
- Share your MCP service implementations as examples
- Contribute additional domain examples that others might find useful

## 📝 License

This template is provided under the MIT License. See `LICENSE` file for details.

---

## 🎉 Template Customization Checklist

### ⚡ Quick Option
- [ ] Run `python3 setup_template.py` for automated setup

### 📋 Manual Option (if not using automated setup)
- [ ] Update `pyproject.toml` with your service details
- [ ] Rename `{{service_name}}_mcp` directory to your service name
- [ ] Update `mcp_instance.py` with your service title and description
- [ ] Replace example domains with your actual business domains
- [ ] Customize prompts in `core/prompts/` directory
- [ ] Update `server.py` to import your tool modules
- [ ] Configure your data connections and authentication
- [ ] Write domain-specific tests
- [ ] Update documentation for your use case
- [ ] Configure CI/CD pipelines for your repository
- [ ] Set up monitoring and alerting for production deployment

**Happy MCP Development! 🚀**
