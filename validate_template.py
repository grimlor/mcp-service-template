#!/usr/bin/env python3
"""
Template Validation Script

This script validates that the MCP service template is properly set up
and ready for users to clone and customize.

USAGE:
- Template maintainers: Run this to verify template integrity after changes
- Contributors: Use this to validate pull requests before submission  
- CI/CD: Integrate into automated testing pipelines
- Users: Optional - can help verify a clean template download

Run: python3 validate_template.py [--syntax-only]
"""

import sys
from pathlib import Path

def check_file_exists(path: str) -> bool:
    """Check if a file exists."""
    return Path(path).exists()

def check_directory_structure():
    """Check that the expected directory structure exists."""
    print("🔍 Checking directory structure...")
    
    expected_dirs = [
        "src/service_name_mcp",
        "src/service_name_mcp/common",
        "src/service_name_mcp/core",
        "src/service_name_mcp/sqlite_domain",
        "src/service_name_mcp/rest_api_domain", 
        "src/service_name_mcp/file_processing_domain",
        "src/service_name_mcp/docs_domain",
        "src/service_name_mcp/analytics_domain",
        "tests",
        "tests/test_sqlite_domain",
        "tests/test_rest_api_domain",
        "tests/test_file_processing_domain",
        "tests/test_docs_domain",
        "tests/test_analytics_domain",
        "docs"
    ]
    
    missing_dirs = []
    for directory in expected_dirs:
        if not Path(directory).is_dir():
            missing_dirs.append(directory)
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    else:
        print("✅ All expected directories present")
        return True

def check_essential_files():
    """Check that essential files exist."""
    print("🔍 Checking essential files...")
    
    essential_files = [
        "README.md",
        "pyproject.toml",
        "setup_template.py",
        "src/service_name_mcp/__init__.py",
        "src/service_name_mcp/server.py",
        "src/service_name_mcp/mcp_instance.py",
        "tests/test_server.py"
    ]
    
    missing_files = []
    for file_path in essential_files:
        if not check_file_exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing essential files: {missing_files}")
        return False
    else:
        print("✅ All essential files present")
        return True

def check_domain_completeness():
    """Check that each domain has required files."""
    print("🔍 Checking domain completeness...")
    
    domains = ["sqlite_domain", "rest_api_domain", "file_processing_domain", "docs_domain", "analytics_domain"]
    
    issues = []
    for domain in domains:
        # Check for tools file
        tools_file = f"src/service_name_mcp/{domain}/{domain.replace('_domain', '_tools')}.py"
        if not check_file_exists(tools_file):
            issues.append(f"Missing {tools_file}")
        
        # Check for test directory
        test_dir = f"tests/test_{domain}"
        if not Path(test_dir).is_dir():
            issues.append(f"Missing test directory {test_dir}")
        
        # Check for test file
        test_file = f"tests/test_{domain}/test_{domain.replace('_domain', '_tools')}.py"
        if not check_file_exists(test_file):
            issues.append(f"Missing {test_file}")
    
    if issues:
        print(f"❌ Domain issues: {issues}")
        return False
    else:
        print("✅ All domains complete")
        return True

def check_azure_removal():
    """Check that Azure-specific references have been removed."""
    print("🔍 Checking for Azure-specific references...")
    
    # Check common files for Azure references
    files_to_check = [
        "src/service_name_mcp/common/config.py",
        "src/service_name_mcp/docs_domain/docs_tools.py",
        "README.md"
    ]
    
    azure_refs = []
    for file_path in files_to_check:
        if check_file_exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                # Check for Azure-specific terms that shouldn't be in a general template
                problematic_terms = ["AZURE_TENANT_ID", "AZURE_CLIENT_ID", "kusto_domain", "semantic_model_domain"]
                for term in problematic_terms:
                    if term in content:
                        azure_refs.append(f"{file_path}: {term}")
    
    if azure_refs:
        print(f"❌ Found Azure-specific references: {azure_refs}")
        return False
    else:
        print("✅ No problematic Azure references found")
        return True

def check_python_syntax():
    """Check that all Python files have valid syntax."""
    print("🔍 Checking Python syntax...")
    
    python_files = []
    
    # Find all Python files
    for pattern in ["src/**/*.py", "tests/**/*.py", "*.py"]:
        python_files.extend(Path(".").glob(pattern))
    
    syntax_errors = []
    for py_file in python_files:
        try:
            with open(py_file, 'r') as f:
                compile(f.read(), py_file, 'exec')
        except SyntaxError as e:
            syntax_errors.append(f"{py_file}: {e}")
        except Exception as e:
            syntax_errors.append(f"{py_file}: {e}")
    
    if syntax_errors:
        print("❌ Python syntax errors found:")
        for error in syntax_errors:
            print(f"  {error}")
        return False
    else:
        print("✅ All Python files have valid syntax")
        return True


def check_template_placeholders():
    """Check that template placeholders are present."""
    print("🔍 Checking template placeholders...")
    
    # Check that placeholders exist in key files
    key_files = [
        "src/service_name_mcp/__init__.py",
        "src/service_name_mcp/mcp_instance.py", 
        "README.md"
    ]
    
    missing_placeholders = []
    for file_path in key_files:
        if check_file_exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if "{{service_name}}" not in content and "{{Service Name}}" not in content:
                    missing_placeholders.append(file_path)
    
    if missing_placeholders:
        print(f"❌ Missing template placeholders in: {missing_placeholders}")
        return False
    else:
        print("✅ Template placeholders present")
        return True

def main():
    """Run all validation checks."""
    print("🎯 MCP Service Template Validation")
    print("=" * 40)
    
    checks = [
        check_directory_structure,
        check_essential_files,
        check_domain_completeness,
        check_azure_removal,
        check_python_syntax,
        check_template_placeholders
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Error running {check.__name__}: {e}")
            results.append(False)
            print()
    
    print("=" * 40)
    if all(results):
        print("🎉 Template validation PASSED!")
        print("✅ Template is ready for users to clone and customize")
        return 0
    else:
        print("❌ Template validation FAILED!")
        print("🔧 Please fix the issues above before distributing the template")
        return 1

if __name__ == "__main__":
    # Simple command-line support for syntax-only checking
    if len(sys.argv) > 1 and sys.argv[1] == "--syntax-only":
        print("🎯 MCP Service Template - Syntax Check Only")
        print("=" * 40)
        result = check_python_syntax()
        print("\n" + "=" * 40)
        if result:
            print("🎉 Python syntax check PASSED!")
            sys.exit(0)
        else:
            print("❌ Python syntax check FAILED!")
            sys.exit(1)
    else:
        sys.exit(main())
