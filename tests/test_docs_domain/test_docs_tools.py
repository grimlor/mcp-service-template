"""
Test suite for Documentation Domain

This module contains unit tests for documentation search and retrieval tools.
"""

from unittest.mock import patch

import pytest

# Note: These tests use the template placeholders and will work after setup_template.py is run


class TestDocsTools:
    """Test documentation domain functionality."""

    def test_docs_tools_import(self):
        """Test that docs tools can be imported."""
        try:
            from service_name_mcp.docs_domain import docs_tools

            assert docs_tools is not None
        except ImportError as e:
            pytest.fail(f"Failed to import docs tools: {e}")

    @patch("service_name_mcp.docs_domain.docs_tools.logger")
    def test_search_documentation_success(self, mock_logger):
        """Test successful documentation search."""
        from service_name_mcp.docs_domain.docs_tools import search_documentation

        result = search_documentation(search_text="API endpoints")

        assert isinstance(result, list)
        # Should return mock results from template
        assert len(result) > 0

        # Check result structure
        for item in result:
            assert isinstance(item, dict)
            assert "fileName" in item
            assert "path" in item
            assert "contentSnippet" in item
            assert "score" in item

        mock_logger.info.assert_called()

    @patch("service_name_mcp.docs_domain.docs_tools.logger")
    def test_search_documentation_with_filter(self, mock_logger):
        """Test documentation search with path filter."""
        from service_name_mcp.docs_domain.docs_tools import search_documentation

        result = search_documentation(
            search_text="configuration", path_filter="/docs/{{service_name}}/config/", max_results=5
        )

        assert isinstance(result, list)
        assert len(result) <= 5
        mock_logger.info.assert_called()

    @patch("service_name_mcp.docs_domain.docs_tools.logger")
    def test_search_documentation_empty_query(self, mock_logger):
        """Test documentation search with empty query."""
        from service_name_mcp.docs_domain.docs_tools import search_documentation

        result = search_documentation(search_text="")

        assert isinstance(result, list)
        # Should handle empty query gracefully
        mock_logger.info.assert_called()

    @patch("service_name_mcp.docs_domain.docs_tools.logger")
    def test_fetch_documentation_page_success(self, mock_logger):
        """Test successful documentation page fetching."""
        from service_name_mcp.docs_domain.docs_tools import fetch_documentation_page

        result = fetch_documentation_page(file_path="/docs/{{service_name}}/api/endpoints.md")

        assert isinstance(result, str)
        assert len(result) > 0
        # Should contain mock content from template
        assert "{{Service Name}}" in result or "Documentation" in result
        mock_logger.info.assert_called()

    @patch("service_name_mcp.docs_domain.docs_tools.logger")
    def test_fetch_documentation_page_various_paths(self, mock_logger):
        """Test fetching documentation pages with various path formats."""
        from service_name_mcp.docs_domain.docs_tools import fetch_documentation_page

        test_paths = [
            "/docs/overview.md",
            "concepts/architecture.md",
            "/api/reference/endpoints.md",
            "best-practices/security.md",
        ]

        for path in test_paths:
            result = fetch_documentation_page(file_path=path)
            assert isinstance(result, str)
            assert len(result) > 0

        # Should have made multiple logging calls
        assert mock_logger.info.call_count >= len(test_paths)

    def test_search_result_filtering(self):
        """Test search result filtering logic."""
        from service_name_mcp.docs_domain.docs_tools import search_documentation

        # Test search with specific terms
        result = search_documentation(search_text="overview")

        assert isinstance(result, list)

        # Check that results contain relevant content
        # (This tests the mock filtering logic in the template)
        if result:  # If there are results
            for item in result:
                content = item.get("contentSnippet", "").lower()
                # The mock should filter based on search terms
                assert "overview" in content or "concept" in content or "api" in content

    def test_documentation_constants(self):
        """Test documentation configuration constants."""
        from service_name_mcp.docs_domain.docs_tools import (
            DEFAULT_ORGANIZATION,
            DEFAULT_PATH,
            DEFAULT_PROJECT,
            DEFAULT_REPOSITORY,
        )

        # Verify constants are defined
        assert DEFAULT_ORGANIZATION is not None
        assert DEFAULT_PROJECT is not None
        assert DEFAULT_REPOSITORY is not None
        assert DEFAULT_PATH is not None

        # Verify they have reasonable values
        assert isinstance(DEFAULT_ORGANIZATION, str)
        assert isinstance(DEFAULT_PROJECT, str)
        assert isinstance(DEFAULT_REPOSITORY, str)
        assert isinstance(DEFAULT_PATH, str)


class TestSearchFunctionality:
    """Test documentation search functionality."""

    def test_boolean_search_patterns(self):
        """Test various search patterns and operators."""
        from service_name_mcp.docs_domain.docs_tools import search_documentation

        test_queries = [
            "API AND endpoints",
            "configuration OR setup",
            "database NOT deprecated",
            "(api OR endpoint) AND authentication",
            "config*",
            "set?",
        ]

        for query in test_queries:
            result = search_documentation(search_text=query)
            assert isinstance(result, list)
            # Each query should return some results (from mock)
            # This tests that the search function handles various query formats

    def test_search_result_scoring(self):
        """Test search result scoring and ranking."""
        from service_name_mcp.docs_domain.docs_tools import search_documentation

        result = search_documentation(search_text="API")

        if result:  # If there are results
            # Check that results have scores
            for item in result:
                assert "score" in item
                assert isinstance(item["score"], int | float)
                assert item["score"] >= 0

            # Check that results are sorted by score (descending)
            scores = [item["score"] for item in result]
            assert scores == sorted(scores, reverse=True)

    def test_max_results_limit(self):
        """Test that max_results parameter is respected."""
        from service_name_mcp.docs_domain.docs_tools import search_documentation

        # Test with different limits
        for limit in [1, 5, 10]:
            result = search_documentation(search_text="documentation", max_results=limit)
            assert len(result) <= limit


class TestDocumentationRetrieval:
    """Test documentation content retrieval."""

    def test_page_content_structure(self):
        """Test the structure of retrieved page content."""
        from service_name_mcp.docs_domain.docs_tools import fetch_documentation_page

        result = fetch_documentation_page(file_path="/docs/overview.md")

        assert isinstance(result, str)

        # Check for markdown structure indicators
        # (Based on the mock content in the template)
        assert "#" in result  # Should have headers
        assert "##" in result  # Should have subheaders

        # Check for expected sections
        assert "Overview" in result
        assert "Implementation" in result or "Example" in result

    def test_error_handling_for_invalid_paths(self):
        """Test error handling for invalid file paths."""
        from service_name_mcp.docs_domain.docs_tools import fetch_documentation_page

        # The template implementation should handle various path formats
        # These shouldn't cause crashes
        test_paths = [
            "",
            "/",
            "nonexistent/path.md",
            "../../../etc/passwd",  # Path traversal attempt
            "special chars !@#$.md",
        ]

        for path in test_paths:
            try:
                result = fetch_documentation_page(file_path=path)
                # Should return some content even for invalid paths (mock implementation)
                assert isinstance(result, str)
            except Exception:
                # Errors are acceptable for invalid paths
                pass


class TestDocumentationWorkflow:
    """Test end-to-end documentation workflows."""

    @patch("service_name_mcp.docs_domain.docs_tools.logger")
    def test_search_and_fetch_workflow(self, mock_logger):
        """Test complete search and fetch workflow."""
        from service_name_mcp.docs_domain.docs_tools import fetch_documentation_page, search_documentation

        # 1. Search for documentation
        search_results = search_documentation(search_text="API authentication")

        assert isinstance(search_results, list)

        # 2. Fetch content from search results
        if search_results:
            first_result = search_results[0]
            file_path = first_result["path"]

            content = fetch_documentation_page(file_path=file_path)
            assert isinstance(content, str)
            assert len(content) > 0

        # Verify logging occurred for both operations
        assert mock_logger.info.call_count >= 2

    def test_multiple_page_fetching(self):
        """Test fetching multiple documentation pages."""
        from service_name_mcp.docs_domain.docs_tools import fetch_documentation_page

        # Simulate fetching multiple pages based on search results
        pages = ["/docs/api/endpoints.md", "/docs/concepts/overview.md", "/docs/best-practices.md"]

        contents = []
        for page in pages:
            content = fetch_documentation_page(file_path=page)
            contents.append(content)
            assert isinstance(content, str)
            assert len(content) > 0

        # Verify we got different content for different pages
        # (The mock implementation includes the file path in the content)
        for i, content in enumerate(contents):
            assert pages[i] in content


class TestDocumentationIntegration:
    """Integration tests for documentation domain."""

    def test_mcp_tool_registration(self):
        """Test that documentation tools are properly registered with MCP."""
        try:
            # Import the tools module to trigger registration
            from service_name_mcp.mcp_instance import mcp

            # This test verifies that import doesn't fail
            assert mcp is not None

        except ImportError as e:
            pytest.fail(f"Failed to register documentation tools with MCP: {e}")

    @pytest.mark.integration
    def test_documentation_tool_descriptions(self):
        """Test that tools have proper descriptions for MCP."""
        # This would test the actual MCP tool registration
        # For now, we just verify the modules can be imported
        from service_name_mcp.docs_domain.docs_tools import fetch_documentation_page, search_documentation

        # Verify functions exist and are callable
        assert callable(search_documentation)
        assert callable(fetch_documentation_page)

        # Verify they have docstrings (important for MCP tool descriptions)
        assert search_documentation.__doc__ is not None
        assert fetch_documentation_page.__doc__ is not None
        assert len(search_documentation.__doc__) > 50
        assert len(fetch_documentation_page.__doc__) > 50


class TestDocumentationConfiguration:
    """Test documentation configuration and setup."""

    def test_default_configuration_values(self):
        """Test that default configuration is properly set."""
        from service_name_mcp.docs_domain.docs_tools import (
            DEFAULT_ORGANIZATION,
            DEFAULT_PATH,
            DEFAULT_PROJECT,
            DEFAULT_REPOSITORY,
        )

        # Verify placeholders are present (will be replaced by setup script)
        assert "your_" in DEFAULT_ORGANIZATION or "{{" in DEFAULT_ORGANIZATION
        assert "your_" in DEFAULT_PROJECT or "{{" in DEFAULT_PROJECT
        assert "your_" in DEFAULT_REPOSITORY or "{{" in DEFAULT_REPOSITORY
        assert "/docs/" in DEFAULT_PATH

    def test_customization_guidance(self):
        """Test that customization guidance is present in the code."""
        import inspect

        from service_name_mcp.docs_domain import docs_tools

        # Get the source code to check for TODO comments
        source = inspect.getsource(docs_tools)

        # Should contain guidance for customization
        assert "TODO" in source
        assert "Implement your" in source or "customize" in source.lower()


if __name__ == "__main__":
    pytest.main([__file__])
