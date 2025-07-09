# Development Guide

This guide covers the daily development workflow for MCP service projects created from this template.

## 🚀 Quick Start

After running `python3 setup_template.py`, navigate to your project directory and follow these steps:

### 1. Prerequisites

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install direnv (recommended for automatic environment activation)
# macOS: brew install direnv
# Ubuntu/Debian: sudo apt install direnv
# Configure: eval "$(direnv hook zsh)" in your shell profile
```

### 2. Environment Setup

#### Option A: Automatic (Recommended with direnv)
```bash
# Navigate to project and allow direnv
cd your-project/
direnv allow

# Environment auto-activates with all dependencies!
# You'll see helpful output about available commands
```

#### Option B: Manual
```bash
# Create virtual environment and install dependencies
uv sync --all-extras

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Set up pre-commit hooks
uv run pre-commit install

# Add project to Python path
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
```

## 🔄 Understanding the direnv Workflow

When using direnv (recommended), the `.envrc` file automatically:

1. **Environment Activation**: Creates and activates the virtual environment
2. **Dependency Management**: Runs `uv sync --all-extras` to install dependencies
3. **Pre-commit Setup**: Installs pre-commit hooks automatically
4. **Path Configuration**: Sets up PYTHONPATH and other environment variables
5. **Helpful Output**: Shows available commands when entering the directory

### What You'll See
```bash
$ cd your-project/
direnv: loading ~/your-project/.envrc
🔄 Syncing dependencies...
✅ Environment activated!
🚀 Available commands:
   uv run pytest                 # Run tests
   uv run ruff check             # Lint code
   uv run ruff format src/       # Format code
   uv run mypy src/              # Type check
   uv run pre-commit run --all-files  # Run all quality checks

$ # Now you can run commands directly!
$ uv run pytest
```

### Direnv Commands
```bash
# Allow direnv for this project (first time)
direnv allow

# Reload environment (after changing .envrc)
direnv reload

# Check status
direnv status

# Temporarily disable
direnv deny
```

## 🛠️ Development Workflow

### Code Quality Commands

```bash
# Format code
uv run ruff format src/ tests/

# Check linting and style
uv run ruff check src/ tests/

# Auto-fix linting issues
uv run ruff check src/ tests/ --fix

# Type checking
uv run mypy src/
```

### Testing Commands

```bash
# Run all tests
uv run pytest

# Run tests with coverage report
uv run pytest --cov

# Generate detailed HTML coverage report
uv run pytest --cov --cov-report=html
# Opens htmlcov/index.html in your browser to see detailed coverage

# Run tests and fail if coverage is below 80% (our target)
uv run pytest --cov --cov-fail-under=80

# Run only unit tests (skip slow integration tests)
uv run pytest -m "not integration"

# Run specific test file
uv run pytest tests/test_server.py -v

# Run tests with debugging output
uv run pytest -s --tb=long

# Run tests in parallel (faster, requires pytest-xdist)
uv run pytest -n auto

# Generate XML coverage report (for CI/CD)
uv run pytest --cov --cov-report=xml
```

# Run specific domain tests
uv run pytest tests/test_your_domain/

# Run integration tests only
uv run pytest tests/integration/
```

### Running Your Service

```bash
# Start the MCP server
uv run python3 -m your_service_mcp.server
```

## 🔧 Alternative: Traditional pip Workflow

If you prefer using pip instead of uv:

```bash
# Install in development mode
pip install -e ".[dev]"

# Activate virtual environment (if using one)
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Then use commands without 'uv run' prefix
ruff format src/ tests/
pytest
mypy src/
```

## 🪝 Automated Quality Checks

The template includes pre-commit hooks that run automatically before each commit:

- **Code formatting** with `ruff format`
- **Linting and style** with `ruff check --fix`
- **Type checking** with `mypy`
- **File consistency** (trailing whitespace, line endings, etc.)

Run manually on all files:
```bash
uv run pre-commit run --all-files
```

## 🔧 Troubleshooting

### Common Issues

**uv not found**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart terminal or source shell config
```

**Missing dependencies**
```bash
# Reinstall all dependencies
uv sync --all-extras

# Or if using direnv
direnv reload
```

**Virtual environment issues**
```bash
# Delete and recreate virtual environment
rm -rf .venv/
uv sync --all-extras

# Or with direnv
direnv reload
```

**Import errors after setup**
```bash
# Ensure setup completed successfully
# Check that all {{placeholders}} were replaced
# Verify directory renaming was successful
```

**Tests failing**
```bash
# Run specific test to debug
uv run pytest tests/test_specific_file.py -v

# Run with debugging output
uv run pytest -s --tb=long
```

**Type checking errors**
```bash
# Run mypy with verbose output
uv run mypy src/ --show-error-codes

# Ignore specific errors temporarily
# Add # type: ignore[error-code] comments
```

## 🎯 Best Practices

### Daily Workflow
1. **Pull latest changes**: `git pull`
2. **Update dependencies**: `uv sync --all-extras` (if pyproject.toml changed, or `direnv reload`)
3. **Make your changes**
4. **Run quality checks**: `uv run pre-commit run --all-files`
5. **Run tests**: `uv run pytest`
6. **Commit changes**: `git commit -m "Your message"` (hooks run automatically)

### Before Submitting PR
1. **Format and lint**: `uv run ruff format . && uv run ruff check . --fix`
2. **Type check**: `uv run mypy src/`
3. **Full test suite**: `uv run pytest --cov=src/`
4. **Test your changes**: Manual testing of modified functionality

### Performance Tips
- **Use uv for speed**: 10-100x faster than pip
- **Parallel testing**: `uv run pytest -n auto` (requires pytest-xdist)
- **Incremental mypy**: `uv run mypy src/ --incremental`

## 📚 Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [direnv Documentation](https://direnv.net/)
- [Model Context Protocol](https://github.com/anthropics/mcp)
- [FastMCP Documentation](https://github.com/mcp-host/fastmcp)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [pre-commit Documentation](https://pre-commit.com/)
