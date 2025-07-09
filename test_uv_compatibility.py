#!/usr/bin/env python3
"""
MCP Template Validation Script

This script validates that the MCP service template works correctly with uv
after the setup process. It can be used by:

1. Template maintainers to test changes
2. Users to validate their setup worked correctly
3. CI/CD pipelines to ensure template quality

Usage:
    python3 test_uv_compatibility.py

The script will create a temporary copy of the template, run the setup process,
and validate that uv can successfully install dependencies and run commands.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def test_uv_after_setup():
    """Test that uv works after template setup"""
    print("🧪 Testing uv compatibility after template setup...")

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        template_copy = temp_path / "test_template"

        # Copy template to temp directory
        current_dir = Path(__file__).parent
        shutil.copytree(current_dir, template_copy, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))

        print(f"📁 Created test copy in: {template_copy}")

        # Run setup script with test values
        print("🔧 Running setup script...")

        # Create input for setup script
        setup_input = "test_service\nTest Service\nTest service for validation\nTest Domain\n\n\n"

        success, stdout, stderr = run_command(f"echo '{setup_input}' | python3 setup_template.py", cwd=template_copy)

        if not success:
            print(f"❌ Setup script failed: {stderr}")
            return False

        print("✅ Setup script completed")

        # Check if uv can now parse the project
        print("📦 Testing uv sync...")
        success, stdout, stderr = run_command("uv sync --all-extras", cwd=template_copy)

        if success:
            print("✅ uv sync successful")

            # Test running a simple command
            print("🧪 Testing uv run...")
            success, stdout, stderr = run_command(
                "uv run python3 -c 'import test_service_mcp; print(\"Import successful\")'", cwd=template_copy
            )

            if success:
                print("✅ uv run successful")
                return True
            else:
                print(f"❌ uv run failed: {stderr}")
                return False
        else:
            print(f"❌ uv sync failed: {stderr}")
            return False


if __name__ == "__main__":
    if test_uv_after_setup():
        print("\n🎉 All tests passed! Template is uv-compatible after setup.")
        sys.exit(0)
    else:
        print("\n💥 Tests failed!")
        sys.exit(1)
