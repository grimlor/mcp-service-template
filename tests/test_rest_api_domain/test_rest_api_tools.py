"""
Test suite for REST API Domain

This module contains unit tests for REST API integration tools.
"""

import pytest
import json
from unittest.mock import patch, MagicMock, Mock
import requests

# Note: These tests use the template placeholders and will work after setup_template.py is run


class TestRestApiTools:
    """Test REST API domain functionality."""
    
    def test_rest_api_tools_import(self):
        """Test that REST API tools can be imported."""
        try:
            from service_name_mcp.rest_api_domain import rest_api_tools
            assert rest_api_tools is not None
        except ImportError as e:
            pytest.fail(f"Failed to import REST API tools: {e}")
    
    @patch('requests.get')
    @patch('service_name_mcp.rest_api_domain.rest_api_tools.logger')
    def test_fetch_data_success(self, mock_logger, mock_get):
        """Test successful data fetching from API."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "data": [{"id": 1, "name": "Test Item"}]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        from service_name_mcp.rest_api_domain.rest_api_tools import fetch_api_data
        
        result = fetch_api_data(
            endpoint="test",
            params={"limit": 10}
        )
        
        assert isinstance(result, dict)
        assert result["status"] == "success"
        mock_get.assert_called_once()
        mock_logger.info.assert_called()
    
    @patch('requests.get')
    @patch('service_name_mcp.rest_api_domain.rest_api_tools.logger')
    def test_fetch_data_http_error(self, mock_logger, mock_get):
        """Test HTTP error handling."""
        # Mock HTTP error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        from service_name_mcp.rest_api_domain.rest_api_tools import fetch_api_data
        
        with pytest.raises(Exception):
            fetch_api_data(endpoint="nonexistent")
        
        mock_logger.error.assert_called()
    
    @patch('requests.get')
    @patch('service_name_mcp.rest_api_domain.rest_api_tools.logger')
    def test_fetch_data_timeout(self, mock_logger, mock_get):
        """Test timeout handling."""
        # Mock timeout
        mock_get.side_effect = requests.Timeout("Request timed out")
        
        from service_name_mcp.rest_api_domain.rest_api_tools import fetch_api_data
        
        with pytest.raises(Exception):
            fetch_api_data(endpoint="slow")
        
        mock_logger.error.assert_called()
    
    @patch('requests.get')
    def test_fetch_data_with_parameters(self, mock_get):
        """Test API calls with parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"filtered": "data"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        from service_name_mcp.rest_api_domain.rest_api_tools import fetch_api_data
        
        params = {"category": "electronics", "limit": 5}
        result = fetch_api_data(endpoint="products", params=params)
        
        # Verify the request was made with correct parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "params" in call_args.kwargs
        assert call_args.kwargs["params"] == params
    
    @patch('requests.post')
    @patch('service_name_mcp.rest_api_domain.rest_api_tools.logger')
    def test_post_data_success(self, mock_logger, mock_post):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 123, "status": "created"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        from service_name_mcp.rest_api_domain.rest_api_tools import post_api_data
        
        data = {"name": "New Item", "category": "test"}
        result = post_api_data(endpoint="items", data=data)
        
        assert isinstance(result, dict)
        assert result["status"] == "created"
        mock_post.assert_called_once()
        mock_logger.info.assert_called()
    
    def test_url_construction(self):
        """Test URL construction logic."""
        from service_name_mcp.rest_api_domain.rest_api_tools import _build_url
        
        # Test basic URL construction
        base_url = "https://api.example.com/v1"
        endpoint = "users"
        
        url = _build_url(base_url, endpoint)
        assert url == "https://api.example.com/v1/users"
        
        # Test with trailing slash
        url = _build_url("https://api.example.com/v1/", "users")
        assert url == "https://api.example.com/v1/users"
        
        # Test with leading slash in endpoint
        url = _build_url("https://api.example.com/v1", "/users")
        assert url == "https://api.example.com/v1/users"
    
    @patch('requests.get')
    def test_rate_limiting_handling(self, mock_get):
        """Test rate limiting response handling."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "60"}
        mock_response.raise_for_status.side_effect = requests.HTTPError("429 Too Many Requests")
        mock_get.return_value = mock_response
        
        from service_name_mcp.rest_api_domain.rest_api_tools import fetch_api_data
        
        with pytest.raises(Exception) as exc_info:
            fetch_api_data(endpoint="rate-limited")
        
        # Should contain rate limiting information
        assert "429" in str(exc_info.value) or "rate" in str(exc_info.value).lower()


class TestApiConfiguration:
    """Test API configuration and settings."""
    
    def test_default_configuration(self):
        """Test default API configuration."""
        from service_name_mcp.rest_api_domain.rest_api_tools import DEFAULT_BASE_URL, DEFAULT_TIMEOUT
        
        assert DEFAULT_BASE_URL is not None
        assert isinstance(DEFAULT_TIMEOUT, (int, float))
        assert DEFAULT_TIMEOUT > 0
    
    def test_headers_configuration(self):
        """Test request headers configuration."""
        from service_name_mcp.rest_api_domain.rest_api_tools import _get_default_headers
        
        headers = _get_default_headers()
        assert isinstance(headers, dict)
        assert "User-Agent" in headers
        assert "Accept" in headers


class TestDataProcessing:
    """Test data processing and transformation."""
    
    def test_json_response_processing(self):
        """Test JSON response processing."""
        from service_name_mcp.rest_api_domain.rest_api_tools import _process_response
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value", "list": [1, 2, 3]}
        
        result = _process_response(mock_response)
        assert isinstance(result, dict)
        assert result["key"] == "value"
        assert result["list"] == [1, 2, 3]
    
    def test_pagination_handling(self):
        """Test pagination response handling."""
        from service_name_mcp.rest_api_domain.rest_api_tools import _extract_pagination_info
        
        response_data = {
            "data": [{"id": 1}, {"id": 2}],
            "pagination": {
                "page": 1,
                "total_pages": 5,
                "total_items": 100
            }
        }
        
        pagination = _extract_pagination_info(response_data)
        assert pagination["page"] == 1
        assert pagination["total_pages"] == 5
        assert pagination["total_items"] == 100


class TestBestPractices:
    """Test REST API best practices and documentation."""
    
    def test_best_practices_file_exists(self):
        """Test that best practices documentation exists."""
        from pathlib import Path
        
        # Get the path to the best practices file
        current_dir = Path(__file__).parent.parent.parent
        best_practices_path = current_dir / "src" / "service_name_mcp" / "rest_api_domain" / "best_practices.md"
        
        assert best_practices_path.exists(), "REST API best practices file should exist"
        
        # Verify it has content
        content = best_practices_path.read_text()
        assert len(content) > 100, "Best practices should have substantial content"
        assert any(keyword in content.lower() for keyword in ["api", "rest", "http"]), \
            "Best practices should mention API concepts"


# Integration tests
class TestRestApiIntegration:
    """Integration tests for REST API domain."""
    
    def test_mcp_tool_registration(self):
        """Test that REST API tools are properly registered with MCP."""
        try:
            # Import the tools module to trigger registration
            import service_name_mcp.rest_api_domain.rest_api_tools
            from service_name_mcp.mcp_instance import mcp
            
            # This test verifies that import doesn't fail
            assert mcp is not None
            
        except ImportError as e:
            pytest.fail(f"Failed to register REST API tools with MCP: {e}")
    
    @pytest.mark.integration
    @patch('requests.get')
    def test_end_to_end_api_workflow(self, mock_get):
        """Test complete REST API workflow."""
        # Mock multiple API responses for a workflow
        mock_responses = [
            # First call: get categories
            Mock(status_code=200, **{
                'json.return_value': {"categories": ["electronics", "books"]},
                'raise_for_status': Mock()
            }),
            # Second call: get products in category
            Mock(status_code=200, **{
                'json.return_value': {
                    "products": [
                        {"id": 1, "name": "Laptop", "price": 999},
                        {"id": 2, "name": "Mouse", "price": 29}
                    ]
                },
                'raise_for_status': Mock()
            })
        ]
        mock_get.side_effect = mock_responses
        
        from service_name_mcp.rest_api_domain.rest_api_tools import fetch_api_data
        
        # 1. Get categories
        categories = fetch_api_data(endpoint="categories")
        assert "categories" in categories
        
        # 2. Get products for first category
        products = fetch_api_data(
            endpoint="products",
            params={"category": categories["categories"][0]}
        )
        assert "products" in products
        assert len(products["products"]) > 0
        
        # Verify both API calls were made
        assert mock_get.call_count == 2


if __name__ == "__main__":
    pytest.main([__file__])
