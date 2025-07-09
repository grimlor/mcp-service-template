#!/usr/bin/env python3
"""
Coverage checking script for the MCP service template.
This script helps track progress toward our 80% coverage goal.
"""

import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def get_coverage_data():
    """Get coverage data from existing coverage.xml or run tests to generate it."""

    # First check if coverage.xml already exists
    coverage_file = Path("coverage.xml")

    if not coverage_file.exists():
        print("🧪 Running tests with coverage...")
        # Run tests with XML coverage output
        subprocess.run(
            [
                "uv",
                "run",
                "pytest",
                "--cov=src/service_name_mcp",
                "--cov-report=xml",
                "--cov-report=term-missing",
                "-q",
            ],
            capture_output=True,
            text=True,
        )

        # Note: Don't fail if tests fail - we still want coverage info
        if not coverage_file.exists():
            print("❌ Coverage file not found after running tests")
            return None
    else:
        print("📁 Using existing coverage.xml file")  # Parse coverage.xml
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()

        # Get overall coverage from root element
        if root.tag == "coverage":
            line_rate = float(root.get("line-rate", 0)) * 100
            branch_rate = float(root.get("branch-rate", 0)) * 100

            return {"line_coverage": line_rate, "branch_coverage": branch_rate}
        else:
            print(f"❌ Unexpected root element: {root.tag}")

    except Exception as e:
        print(f"❌ Error parsing coverage file: {e}")

    return None


def main():
    """Main coverage checking function."""
    print("📊 MCP Service Template - Coverage Check")
    print("=" * 50)

    data = get_coverage_data()
    if not data:
        sys.exit(1)

    line_cov = data["line_coverage"]
    branch_cov = data["branch_coverage"]

    print("\n📈 Coverage Results:")
    print(f"   Line Coverage:   {line_cov:.1f}%")
    print(f"   Branch Coverage: {branch_cov:.1f}%")

    # Coverage goals and progress
    goals = [
        (20, "🟥 Getting Started"),
        (40, "🟨 Basic Coverage"),
        (60, "🟦 Good Coverage"),
        (80, "🟩 Excellent Coverage"),
        (90, "🟪 Outstanding Coverage"),
    ]

    print("\n🎯 Progress toward 80% goal:")
    for threshold, label in goals:
        if line_cov >= threshold:
            print(f"   ✅ {label} ({threshold}%)")
        else:
            print(f"   ⏳ {label} ({threshold}%)")
            break

    # Recommendations
    print("\n💡 Recommendations:")
    if line_cov < 20:
        print("   • Start by writing tests for core server functions")
        print("   • Focus on testing the main MCP server entry points")
        print("   • Add tests for configuration and logging")
    elif line_cov < 40:
        print("   • Add tests for utility functions in common/")
        print("   • Test error handling and edge cases")
        print("   • Add integration tests for MCP tools")
    elif line_cov < 60:
        print("   • Test all domain-specific tools")
        print("   • Add tests for complex business logic")
        print("   • Test file I/O and external API interactions")
    elif line_cov < 80:
        print("   • Add tests for error conditions and edge cases")
        print("   • Test all code paths including exception handling")
        print("   • Add property-based tests for complex functions")
    else:
        print("   • Excellent coverage! Consider adding mutation testing")
        print("   • Focus on testing performance and edge cases")
        print("   • Add end-to-end integration tests")

    # Generate HTML report hint
    print("\n📊 For detailed coverage report:")
    print("   uv run pytest --cov --cov-report=html")
    print("   open htmlcov/index.html")

    # Exit with appropriate code
    if line_cov >= 50:  # Current target
        print("\n✅ Coverage target (50%) achieved!")
        sys.exit(0)
    else:
        print(f"\n⚠️  Coverage below target (50%). Current: {line_cov:.1f}%")
        sys.exit(1)


if __name__ == "__main__":
    main()
