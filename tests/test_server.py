"""
Test suite for {{Service Name}} MCP Server

This module contains unit tests for the MCP server core functionality.
"""

from unittest.mock import patch

import pytest


def test_server_imports():
    """Test that all required modules can be imported."""
    try:
        # Test core imports
        from service_name_mcp import __version__
        from service_name_mcp.common.config import config
        from service_name_mcp.common.logging import logger
        from service_name_mcp.mcp_instance import mcp

        # Verify basic functionality
        assert __version__ is not None
        assert mcp is not None
        assert logger is not None
        assert config is not None

    except ImportError as e:
        pytest.fail(f"Failed to import required modules: {e}")


def test_mcp_instance_configuration():
    """Test MCP instance is properly configured."""
    from service_name_mcp.mcp_instance import mcp

    # Test that MCP instance has expected properties
    assert hasattr(mcp, "name")
    assert hasattr(mcp, "instructions")

    # Test configuration values
    assert mcp.name == "FastMCP"  # This is the default name for FastMCP instances
    assert mcp.instructions is not None and len(mcp.instructions) > 0


def test_config_validation():
    """Test configuration validation."""
    from service_name_mcp.common.config import Config

    # Test that config has required attributes
    config = Config()
    assert hasattr(config, "SERVICE_NAME")
    assert hasattr(config, "LOG_LEVEL")

    # Test validation method exists
    assert hasattr(config, "validate")


@pytest.mark.unit
def test_logging_configuration():
    """Test logging is properly configured."""
    from service_name_mcp.common.logging import logger

    # Test logger has required attributes
    assert hasattr(logger, "info")
    assert hasattr(logger, "error")
    assert hasattr(logger, "debug")

    # Test logging works
    logger.info("Test log message")


def test_main_server_function():
    """Test the main server function."""
    with patch("service_name_mcp.mcp_instance.mcp.run") as mock_run:
        from service_name_mcp.server import main

        # Test that main function can be called
        try:
            main()
            mock_run.assert_called_once_with(transport="stdio")
        except SystemExit:
            # Expected when running in test environment
            pass


# TODO: Add more comprehensive tests
# - Test tool registration
# - Test prompt loading
# - Test error handling
# - Test domain-specific functionality
