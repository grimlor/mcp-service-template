# Quick Setup Guide

## 🚀 Automated Setup (Recommended)

The easiest way to customize this template is using the automated setup script:

```bash
python3 setup_template.py
```

**Note**: You must run the setup script first before using `uv sync`, as the template contains placeholders that need to be replaced.

This script will:

1. **Prompt for configuration** - Service name, description, domain, etc.
2. **Replace all placeholders** - Automatically substitute `{{service_name}}`, `{{Service Description}}`, etc.
3. **Rename directories** - Update `service_name_mcp` to your actual service name
4. **Update imports** - Fix all import statements throughout the codebase
5. **Clean up** - Remove template-specific files

### What You'll Be Asked

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

Service name (snake_case, e.g., 'payment_analytics'): my_analytics
Service display name (e.g., 'Payment Analytics'): My Analytics Service
Service description (e.g., 'Advanced payment data analytics'): Custom analytics for my domain
Business domain (title case, e.g., 'Payment Analytics'): My Analytics
Author name (optional): John Doe
Author email (optional): john@example.com

🔄 Processing Template...

📋 Found 47 files to process
  ✏️  Updated: pyproject.toml
  ✏️  Updated: README.md
  ...

📁 Renaming directories...
  📁 Renaming: src/service_name_mcp → src/my_analytics_mcp

🔗 Updating import statements...
  🔗 Updated imports in: src/my_analytics_mcp/server.py
  ...

✅ Setup Complete!
```

## 📋 Manual Setup (Alternative)

If you prefer manual customization, see the detailed instructions in [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md).

## 🚀 After Setup

1. **Install uv** (if not already installed):
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or via pip
   pip install uv
   ```

2. **Install dependencies**:
   ```bash
   # Recommended (faster, better dependency resolution)
   uv sync --all-extras
   
   # Alternative (traditional pip)
   pip install -e ".[dev]"
   ```

3. **Run tests**:
   ```bash
   # With uv
   uv run pytest
   
   # Or activate virtual environment first
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate   # Windows
   pytest
   ```

4. **Start customizing**:
   - Remove unused domain modules from `src/your_service_mcp/`
   - Implement your specific tools and logic
   - Update documentation and tests

5. **Test your MCP server**:
   ```bash
   # With uv
   uv run python3 -m your_service_mcp.server
   
   # Or with activated environment
   python3 -m your_service_mcp.server
   ```

## 🔧 Troubleshooting

- **uv not found**: Install uv first using the instructions above
- **Import errors**: Make sure all references to the old service name have been updated
- **Missing dependencies**: Run `uv sync --all-extras` to install all dependencies
- **Virtual environment issues**: Delete `.venv/` and run `uv sync --all-extras` again
- **File permissions**: Ensure the setup script has execute permissions (`chmod +x setup_template.py`)
- **Template already setup**: The script will warn if placeholders have already been replaced

---

Happy MCP development! 🎉
