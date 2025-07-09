#!/usr/bin/env python3
"""
MCP Service Template Setup Script

This script prompts for service configuration and replaces all template placeholders
throughout the codebase with actual values.
"""

import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List


class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header():
    """Print welcome header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}🚀 MCP Service Template Setup{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 50}{Colors.END}\n")
    print("This script will customize the MCP service template for your specific use case.")
    print("It will prompt for configuration values and replace all template placeholders.\n")


def validate_python_identifier(name: str) -> bool:
    """Validate that the name is a valid Python identifier"""
    return name.isidentifier() and not name.startswith('_')


def validate_service_name(name: str) -> bool:
    """Validate service name (alphanumeric, underscores, hyphens)"""
    return re.match(r'^[a-z][a-z0-9_-]*$', name) is not None


def prompt_for_values() -> Dict[str, str]:
    """Prompt user for all template values"""
    values = {}
    
    print(f"{Colors.BOLD}📝 Service Configuration{Colors.END}\n")
    
    # Service name (snake_case)
    while True:
        service_name = input(f"{Colors.YELLOW}Service name (snake_case, e.g., 'payment_analytics'): {Colors.END}").strip()
        if not service_name:
            print(f"{Colors.RED}❌ Service name cannot be empty{Colors.END}")
            continue
        if not validate_service_name(service_name):
            print(f"{Colors.RED}❌ Service name must be lowercase, start with a letter, and contain only letters, numbers, underscores, and hyphens{Colors.END}")
            continue
        if not validate_python_identifier(service_name):
            print(f"{Colors.RED}❌ Service name must be a valid Python identifier{Colors.END}")
            continue
        values['service_name'] = service_name
        break
    
    # Service display name
    while True:
        display_name = input(f"{Colors.YELLOW}Service display name (e.g., 'Payment Analytics'): {Colors.END}").strip()
        if not display_name:
            print(f"{Colors.RED}❌ Display name cannot be empty{Colors.END}")
            continue
        values['Service Name'] = display_name
        break
    
    # Service description
    while True:
        description = input(f"{Colors.YELLOW}Service description (e.g., 'Advanced payment data analytics'): {Colors.END}").strip()
        if not description:
            print(f"{Colors.RED}❌ Description cannot be empty{Colors.END}")
            continue
        values['Service Description'] = description
        break
    
    # Domain name (title case)
    while True:
        domain = input(f"{Colors.YELLOW}Business domain (title case, e.g., 'Payment Analytics'): {Colors.END}").strip()
        if not domain:
            print(f"{Colors.RED}❌ Domain cannot be empty{Colors.END}")
            continue
        values['Domain'] = domain
        values['domain'] = domain.lower()
        break
    
    # Author name (optional)
    author = input(f"{Colors.YELLOW}Author name (optional): {Colors.END}").strip()
    if author:
        values['author'] = author
    
    # Package author email (optional)
    email = input(f"{Colors.YELLOW}Author email (optional): {Colors.END}").strip()
    if email:
        values['email'] = email
    
    return values


def find_files_to_process(base_path: Path) -> List[Path]:
    """Find all files that need template processing"""
    files_to_process = []
    
    # Include patterns
    include_patterns = [
        "*.py", "*.md", "*.toml", "*.txt", "*.yml", "*.yaml", "*.json"
    ]
    
    # Exclude patterns
    exclude_patterns = [
        "__pycache__", ".git", ".pytest_cache", "*.pyc", "build", "dist", "*.egg-info"
    ]
    
    for pattern in include_patterns:
        for file_path in base_path.rglob(pattern):
            # Check if file should be excluded
            should_exclude = False
            for exclude_pattern in exclude_patterns:
                if exclude_pattern in str(file_path):
                    should_exclude = True
                    break
            
            if not should_exclude and file_path.is_file():
                files_to_process.append(file_path)
    
    return files_to_process


def replace_placeholders_in_file(file_path: Path, replacements: Dict[str, str]) -> bool:
    """Replace template placeholders in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace all placeholders
        for placeholder, value in replacements.items():
            pattern = f"{{{{{placeholder}}}}}"
            content = content.replace(pattern, value)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error processing {file_path}: {e}{Colors.END}")
        return False
    
    return False


def rename_directories(base_path: Path, old_name: str, new_name: str):
    """Rename directories containing the old service name"""
    old_dir_pattern = f"{old_name}_mcp"
    new_dir_pattern = f"{new_name}_mcp"
    
    # Find directories to rename
    dirs_to_rename = []
    for path in base_path.rglob("*"):
        if path.is_dir() and old_dir_pattern in path.name:
            dirs_to_rename.append(path)
    
    # Sort by depth (deepest first) to avoid conflicts
    dirs_to_rename.sort(key=lambda p: len(p.parts), reverse=True)
    
    for old_path in dirs_to_rename:
        new_path = old_path.parent / old_path.name.replace(old_dir_pattern, new_dir_pattern)
        print(f"  📁 Renaming: {old_path.relative_to(base_path)} → {new_path.relative_to(base_path)}")
        shutil.move(str(old_path), str(new_path))


def update_imports(base_path: Path, old_name: str, new_name: str):
    """Update import statements after renaming directories"""
    old_import = f"{old_name}_mcp"
    new_import = f"{new_name}_mcp"
    
    python_files = list(base_path.rglob("*.py"))
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace import statements
            updated_content = content.replace(old_import, new_import)
            
            if updated_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"  🔗 Updated imports in: {file_path.relative_to(base_path)}")
                
        except Exception as e:
            print(f"{Colors.RED}❌ Error updating imports in {file_path}: {e}{Colors.END}")


def cleanup_template_artifacts(base_path: Path):
    """Remove template-specific files that aren't needed in the final project"""
    artifacts_to_remove = [
        "setup_template.py",  # This script itself
        "test_uv_compatibility.py",  # Template validation script
        "validate_template.py",  # Template maintenance tool (not needed by end users)
    ]
    
    for artifact in artifacts_to_remove:
        artifact_path = base_path / artifact
        if artifact_path.exists():
            artifact_path.unlink()
            print(f"  🗑️  Removed: {artifact}")


def print_summary(values: Dict[str, str], files_processed: int):
    """Print setup summary"""
    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Setup Complete!{Colors.END}")
    print(f"{Colors.GREEN}{'=' * 50}{Colors.END}\n")
    
    print(f"{Colors.BOLD}📋 Configuration Summary:{Colors.END}")
    print(f"  • Service Name: {values['service_name']}")
    print(f"  • Display Name: {values['Service Name']}")
    print(f"  • Description: {values['Service Description']}")
    print(f"  • Domain: {values['Domain']}")
    if 'author' in values:
        print(f"  • Author: {values['author']}")
    if 'email' in values:
        print(f"  • Email: {values['email']}")
    
    print(f"\n{Colors.BOLD}📊 Processing Summary:{Colors.END}")
    print(f"  • Files processed: {files_processed}")
    print(f"  • Directory renamed: service_name_mcp → {values['service_name']}_mcp")
    
    print(f"\n{Colors.BOLD}🚀 Next Steps:{Colors.END}")
    print(f"  1. Install uv (if not installed): {Colors.YELLOW}curl -LsSf https://astral.sh/uv/install.sh | sh{Colors.END}")
    print(f"  2. Install dependencies: {Colors.YELLOW}uv sync --all-extras{Colors.END}")
    print(f"  3. Run tests: {Colors.YELLOW}uv run pytest{Colors.END}")
    print("  4. Update dependencies in pyproject.toml as needed")
    print(f"  5. Test your MCP server: {Colors.YELLOW}uv run python3 -m {values['service_name']}_mcp.server{Colors.END}")
    print(f"\n{Colors.BOLD}💡 Alternative (traditional pip):{Colors.END}")
    print(f"  • Install dependencies: {Colors.YELLOW}pip install -e '.[dev]'{Colors.END}")
    print(f"  • Run tests: {Colors.YELLOW}pytest{Colors.END}")


def main():
    """Main setup function"""
    base_path = Path(__file__).parent.absolute()
    
    print_header()
    
    # Check if this is a template (has placeholder values)
    pyproject_path = base_path / "pyproject.toml"
    if not pyproject_path.exists():
        print(f"{Colors.RED}❌ Error: pyproject.toml not found. Make sure you're running this script from the template root.{Colors.END}")
        sys.exit(1)
    
    with open(pyproject_path, 'r') as f:
        content = f.read()
        if "{{service_name}}" not in content:
            print(f"{Colors.YELLOW}⚠️  This template appears to have already been set up.{Colors.END}")
            response = input("Do you want to continue anyway? (y/N): ").strip().lower()
            if response != 'y':
                print("Setup cancelled.")
                sys.exit(0)
    
    # Get configuration values
    values = prompt_for_values()
    
    print(f"\n{Colors.BOLD}🔄 Processing Template...{Colors.END}\n")
    
    # Find all files to process
    files_to_process = find_files_to_process(base_path)
    print(f"📋 Found {len(files_to_process)} files to process")
    
    # Replace placeholders in files
    files_changed = 0
    for file_path in files_to_process:
        if replace_placeholders_in_file(file_path, values):
            files_changed += 1
            print(f"  ✏️  Updated: {file_path.relative_to(base_path)}")
    
    # Rename directories
    print("\n📁 Renaming directories...")
    rename_directories(base_path, "service_name", values["service_name"])
    
    # Update import statements
    print("\n🔗 Updating import statements...")
    update_imports(base_path, "service_name", values["service_name"])
    
    # Clean up template artifacts
    print("\n🧹 Cleaning up template artifacts...")
    cleanup_template_artifacts(base_path)
    
    # Print summary
    print_summary(values, files_changed)


if __name__ == "__main__":
    main()
