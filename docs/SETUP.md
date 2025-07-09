# Quick Setup Guide

## 🚀 Automated Setup (Recommended)

The easiest way to customize this template is using the automated setup script:

```bash
python3 setup_template.py
```

**Note**: You must run the setup script first before using `uv sync`, as the template contains placeholders that need to be replaced.

This script will:

1. **Create a clean project copy** - Copy template files to your target directory, automatically excluding:
   - Git history and contributor-only files
   - Virtual environments and cache directories
   - IDE settings (.vscode, .idea)
   - Lockfiles (you'll get fresh ones)
   - Build artifacts and temporary files

2. **Prompt for configuration** - Service name, description, domain, etc.
3. **Replace all placeholders** - Automatically substitute `{{service_name}}`, `{{Service Description}}`, etc.
4. **Rename directories** - Update `service_name_mcp` to your actual service name
5. **Update imports** - Fix all import statements throughout the codebase
6. **Generate configuration** - Process `pyproject.toml.template` into working `pyproject.toml`
7. **Set up quality tools** - Create `.pre-commit-config.yaml` for automated checks
8. **Clean up artifacts** - Remove template-specific files you don't need

### What You'll Be Asked

- **Target directory**: Where to create your new project (default: `../my-mcp-service`)
- **Service name** (snake_case): e.g., `payment_analytics`
- **Display name**: e.g., `Payment Analytics`
- **Description**: e.g., `Advanced payment data analytics`
- **Business domain**: e.g., `Payment Analytics`
- **Author details** (optional): Name and email

### Example Run

```
🚀 MCP Service Template Setup
==================================================

This script will customize the MCP service template for your specific use case.
It will prompt for configuration values and replace all template placeholders.

📝 Service Configuration

Target directory (where to create your project) [../my-mcp-service]: ../my-analytics-project
Service name (snake_case, e.g., 'payment_analytics'): my_analytics
Service display name (e.g., 'Payment Analytics'): My Analytics Service
Service description (e.g., 'Advanced payment data analytics'): Custom analytics for my domain
Business domain (title case, e.g., 'Payment Analytics'): My Analytics
Author name (optional): John Doe
Author email (optional): john@example.com

🔄 Creating Project...

📁 Creating clean project copy at: /home/user/my-analytics-project
  📄 Copied: README.md
  📄 Copied: pyproject.toml.template
  ... (excluding .git, .venv, uv.lock, IDE settings, etc.)

� Processing Template Files...

📦 Setting up pyproject.toml...
  ✏️  Created: pyproject.toml from template
  🗑️  Removed: pyproject.toml.template

📋 Found 44 additional files to process
  ✏️  Updated: README.md
  ...

📁 Renaming directories...
  📁 Renaming: src/service_name_mcp → src/my_analytics_mcp

🔗 Updating import statements...
  🔗 Updated imports in: src/my_analytics_mcp/server.py
  ...

🧹 Cleaning up template artifacts...
  🗑️  Removed: setup_template.py
  🗑️  Removed: validate_template.py
  🗑️  Removed: pyproject.toml.template

🪝 Setting up automated quality checks...
  🪝 Created: .pre-commit-config.yaml

✅ Setup Complete!

🎉 Your MCP service 'My Analytics Service' is ready for development!
```

## 📋 Manual Setup (Alternative)

If you prefer manual customization, see the detailed instructions in [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md).

## 🚀 After Setup

### Prerequisites

1. **Install uv** (if not already installed):
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # Or via package managers
   brew install uv       # macOS with Homebrew
   pip install uv        # Via pip (slower)
   ```

2. **Install direnv** (recommended for automatic environment activation):
   ```bash
   # macOS
   brew install direnv

   # Ubuntu/Debian
   sudo apt install direnv

   # Or download from: https://direnv.net/docs/installation.html
   ```

3. **Configure direnv** (one-time setup):
   ```bash
   # Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
   eval "$(direnv hook bash)"    # For bash
   eval "$(direnv hook zsh)"     # For zsh
   ```

### Automatic Environment Setup (Recommended)

If you have `direnv` installed, the environment will activate automatically:

```bash
cd your-mcp-project/
direnv allow    # First time only

# Environment auto-activates! You'll see:
# 🔄 Syncing dependencies...
# ✅ Environment activated!
# 🚀 Available commands:
#    uv run pytest                 # Run tests
#    uv run ruff check             # Lint code
#    ...
```

The `.envrc` file will automatically:
- Create and activate the virtual environment
- Install all dependencies (including dev dependencies)
- Set up pre-commit hooks
- Configure Python path and environment variables

### Manual Environment Setup (Alternative)

If you prefer manual control or don't have `direnv`:

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies (including dev dependencies)
uv sync --all-extras

# Set up pre-commit hooks
uv run pre-commit install

# Add project to Python path
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
```

### Verify Setup

```bash
# Run tests
uv run pytest

# Check code quality
uv run ruff check
uv run mypy src/

# Run the MCP server
uv run python -m your_service_mcp.server
```

## 🛠️ Development Workflow

Once setup is complete, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for:
- Complete development commands
- Testing strategies
- Code quality tools
- Debugging and troubleshooting

## 🔧 Troubleshooting

- **uv not found**: Install uv first using the instructions above
- **direnv not working**: Ensure it's installed and properly configured in your shell
- **Environment not activating**: Run `direnv allow` in the project directory
- **Target directory exists**: The script will ask if you want to overwrite - choose 'y' to continue
- **Import errors**: Ensure the setup completed successfully and all references were updated
- **Missing dependencies**: Run `uv sync --all-extras` to install all dependencies
- **Virtual environment issues**: Delete `.venv/` and run `direnv reload` or `uv sync --all-extras`
- **Permission errors**: Ensure the setup script has execute permissions (`chmod +x setup_template.py`)
- **Template already setup**: The script will warn if placeholders have already been replaced
- **Fresh lockfile needed**: The setup excludes `uv.lock` so you get fresh dependency resolution

---

Happy MCP development! 🎉
