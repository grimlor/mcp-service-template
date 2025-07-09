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
- ✨ **Create a clean project copy** in your target directory
- 🔧 **Replace all template placeholders** automatically
- 📁 **Rename directories and update imports** throughout the codebase
- 🗑️ **Exclude contributor-only files** (git history, caches, IDE settings, lockfiles)
- ⚙️ **Generate fresh configuration** from template files
- 🪝 **Set up automated quality checks** with pre-commit hooks

**After setup, you'll have a completely clean, fully customized MCP service ready for development - no manual cleanup required!**

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

**Quick Start After Setup:**
```bash
# Navigate to your project directory
cd path/to/your/new/project

# Automatic setup with direnv (recommended)
direnv allow

# OR manual setup:
# Create virtual environment and install dependencies
uv sync --all-extras

# Set up automated quality checks
uv run pre-commit install

# Run tests to verify everything works
uv run pytest
```

For complete development workflow, testing commands, troubleshooting, and best practices, see **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)**.

### Automated Quality Checks

The template includes pre-commit hooks that automatically run quality checks before each commit. These ensure consistent code quality and prevent common issues from reaching your repository.

**What the hooks check:**
- 🎨 **Code formatting** with `ruff format` (replaces black)
- 🔍 **Linting and style** with `ruff check --fix` (replaces flake8, isort, and more)
- 🏷️ **Type checking** with `mypy`
- 📝 **File consistency** (trailing whitespace, line endings, etc.)

## 📁 Project Structure

```
mcp-service-template/
├── README.md                           # This file
├── pyproject.toml                      # Package configuration (for contributors)
├── pyproject.toml.template             # Template file (becomes pyproject.toml after setup)
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
    ├── SETUP.md                       # Quick setup guide
    ├── DEVELOPMENT.md                 # Complete development workflow
    ├── ARCHITECTURE.md                # Architectural patterns and design principles
    ├── CUSTOMIZATION.md               # Advanced template customization
    └── examples/
        └── ECOMMERCE_EXAMPLE.md       # E-commerce integration example
```

## 🔧 Key Architectural Patterns

This template follows proven architectural patterns for maintainable, scalable MCP services:

- **🏗️ Modular Domain Organization** - Standardized structure for business domains
- **🎯 Centralized MCP Instance** - Single FastMCP instance shared across domains
- **🔌 Tool Registration Pattern** - Consistent tool implementation and error handling
- **📝 Prompt System Pattern** - File-based prompt templates with structured loading
- **⚙️ Configuration Management** - Environment-based config with validation

For complete architectural patterns, design principles, and implementation examples, see **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**.

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

# Run tests with coverage report
uv run pytest --cov

# Generate HTML coverage report
uv run pytest --cov --cov-report=html
# Open htmlcov/index.html in your browser

# Run tests with coverage and fail if below 80%
uv run pytest --cov --cov-fail-under=80

# Run only fast unit tests (skip integration tests)
uv run pytest -m "not integration"
```

For complete testing commands, coverage options, and debugging tips, see **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)**.

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
# Install locally in development mode with development dependencies
uv sync --all-extras

# Build package
uv build

# Alternative: traditional pip install (if not using uv)
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
3. **Use modern development workflow**:
   ```bash
   # Setup (see docs/DEVELOPMENT.md for complete guide)
   uv sync --all-extras
   uv run pre-commit install

   # Daily workflow
   uv run ruff format src/ tests/
   uv run ruff check src/ tests/ --fix
   uv run mypy src/
   uv run pytest
   ```
4. **Validate your changes**:
   ```bash
   # Ensure template integrity (includes syntax checking)
   python3 validate_template.py

   # For faster syntax-only checking during development
   python3 validate_template.py --syntax-only
   ```
5. **Test the template works end-to-end**:
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
6. **Create your feature branch** (`git checkout -b feature/amazing-feature`)
7. **Commit your changes** (`git commit -m 'Add amazing feature'`)
8. **Push to the branch** (`git push origin feature/amazing-feature`)
9. **Open a Pull Request**

**Note**: The template uses a dual `pyproject.toml` system:
- `pyproject.toml` - For template contributors (this repo)
- `pyproject.toml.template` - Template file that becomes `pyproject.toml` after user setup

This allows both contributors and users to benefit from modern `uv` and `ruff` tooling!

### For Template Users:
- Report issues or suggest improvements via GitHub Issues
- Share your MCP service implementations as examples
- Contribute additional domain examples that others might find useful

## 📝 License

This template is provided under the MIT License. See `LICENSE` file for details.

---

## 🎉 Template Customization Checklist

### ⚡ Quick Option (Recommended)
- [ ] Run `python3 setup_template.py` for fully automated setup
- [ ] Answer the prompts for your service configuration
- [ ] Navigate to your new project directory and start developing!

The automated setup handles everything below automatically, creating a clean, production-ready project.

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
