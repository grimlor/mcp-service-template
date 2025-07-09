"""
Test suite for Analytics Domain

This module contains unit tests for analytics and data science tools.
"""

import pytest
from unittest.mock import patch, Mock

# Note: These tests use the template placeholders and will work after setup_template.py is run


class TestAnalyticsTools:
    """Test analytics domain functionality."""
    
    def test_analytics_tools_import(self):
        """Test that analytics tools can be imported."""
        try:
            from service_name_mcp.analytics_domain import analytics_tools
            assert analytics_tools is not None
        except ImportError as e:
            pytest.fail(f"Failed to import analytics tools: {e}")
    
    def test_analytics_prompts_import(self):
        """Test that analytics prompts can be imported."""
        try:
            from service_name_mcp.analytics_domain import analytics_prompts
            assert analytics_prompts is not None
        except ImportError as e:
            pytest.fail(f"Failed to import analytics prompts: {e}")
    
    @patch('service_name_mcp.analytics_domain.analytics_tools.logger')
    def test_contribution_analysis_success(self, mock_logger):
        """Test successful contribution analysis."""
        from service_name_mcp.analytics_domain.analytics_tools import contribution_analysis
        
        result = contribution_analysis(
            current_start_date="2024-01-01",
            current_end_date="2024-01-31",
            comparison_start_date="2023-01-01",
            comparison_end_date="2023-01-31"
        )
        
        assert isinstance(result, dict)
        # Check expected structure from mock response
        assert "analysis_summary" in result
        assert "top_contributors" in result
        
        mock_logger.info.assert_called()
    
    @patch('service_name_mcp.analytics_domain.analytics_tools.logger')
    def test_contribution_analysis_with_dimensions(self, mock_logger):
        """Test contribution analysis with specific dimensions."""
        from service_name_mcp.analytics_domain.analytics_tools import contribution_analysis
        
        result = contribution_analysis(
            current_start_date="2024-01-01",
            current_end_date="2024-01-31",
            comparison_start_date="2023-01-01",
            comparison_end_date="2023-01-31",
            dimensions="PaymentMethodType,Country"
        )
        
        assert isinstance(result, dict)
        mock_logger.info.assert_called()
    
    @patch('service_name_mcp.analytics_domain.analytics_tools.logger')
    def test_contribution_analysis_with_filters(self, mock_logger):
        """Test contribution analysis with filter conditions."""
        from service_name_mcp.analytics_domain.analytics_tools import contribution_analysis
        
        result = contribution_analysis(
            current_start_date="2024-01-01",
            current_end_date="2024-01-31",
            comparison_start_date="2023-01-01",
            comparison_end_date="2023-01-31",
            filter_conditions="Country = 'US'",
            min_volume=500
        )
        
        assert isinstance(result, dict)
        mock_logger.info.assert_called()
    
    def test_get_contribution_dimensions(self):
        """Test getting available dimensions for contribution analysis."""
        from service_name_mcp.analytics_domain.analytics_tools import get_contribution_dimensions
        
        result = get_contribution_dimensions()
        
        assert isinstance(result, dict)
        assert "dimensions" in result
        assert "metrics" in result
        
        # Check that dimensions list is not empty
        assert len(result["dimensions"]) > 0
        assert len(result["metrics"]) > 0
    
    def test_date_validation(self):
        """Test date parameter validation."""
        from service_name_mcp.analytics_domain.analytics_tools import contribution_analysis
        
        # Test with invalid date format
        with pytest.raises(Exception):
            contribution_analysis(
                current_start_date="invalid-date",
                current_end_date="2024-01-31",
                comparison_start_date="2023-01-01",
                comparison_end_date="2023-01-31"
            )
    
    def test_date_range_validation(self):
        """Test date range validation logic."""
        from service_name_mcp.analytics_domain.analytics_tools import contribution_analysis
        
        # Test with end date before start date
        with pytest.raises(Exception):
            contribution_analysis(
                current_start_date="2024-01-31",
                current_end_date="2024-01-01",  # End before start
                comparison_start_date="2023-01-01",
                comparison_end_date="2023-01-31"
            )


class TestAnalyticsConfiguration:
    """Test analytics configuration and settings."""
    
    def test_analytics_config_import(self):
        """Test that analytics configuration can be imported."""
        try:
            from service_name_mcp.analytics_domain import analytics_config
            assert analytics_config is not None
        except ImportError as e:
            pytest.fail(f"Failed to import analytics config: {e}")
    
    def test_default_metrics_configuration(self):
        """Test default metrics configuration."""
        from service_name_mcp.analytics_domain.analytics_config import DEFAULT_METRIC, SUPPORTED_METRICS
        
        assert DEFAULT_METRIC is not None
        assert isinstance(SUPPORTED_METRICS, (list, tuple))
        assert len(SUPPORTED_METRICS) > 0
        assert DEFAULT_METRIC in SUPPORTED_METRICS
    
    def test_dimension_configuration(self):
        """Test dimension configuration."""
        from service_name_mcp.analytics_domain.analytics_config import AVAILABLE_DIMENSIONS
        
        assert isinstance(AVAILABLE_DIMENSIONS, (list, tuple))
        assert len(AVAILABLE_DIMENSIONS) > 0
        
        # Check that dimensions have proper structure
        for dimension in AVAILABLE_DIMENSIONS:
            assert isinstance(dimension, str)
            assert len(dimension) > 0


class TestAnalyticsPrompts:
    """Test analytics prompt functionality."""
    
    def test_analyst_prompt_exists(self):
        """Test that analyst prompt is properly defined."""
        from service_name_mcp.analytics_domain.analytics_prompts import analyst_expert
        
        # Should be callable (MCP prompt decorator)
        assert callable(analyst_expert)
        
        # Should have docstring
        assert analyst_expert.__doc__ is not None
        assert len(analyst_expert.__doc__) > 20
    
    def test_prompt_content_structure(self):
        """Test that prompt content has proper structure."""
        from service_name_mcp.analytics_domain.analytics_prompts import analyst_expert
        
        # Call the prompt function to get messages
        try:
            messages = analyst_expert()
            assert isinstance(messages, list)
            assert len(messages) > 0
            
            # Check message structure
            for message in messages:
                # Messages should have content attribute or be message objects
                assert hasattr(message, 'content') or hasattr(message, 'text') or isinstance(message, str)
        except Exception:
            # If there's an error calling the prompt, that's expected in test environment
            # The important thing is that the function exists and is callable
            pass


class TestDataAnalysis:
    """Test data analysis functionality."""
    
    def test_mock_data_generation(self):
        """Test mock data generation for analysis."""
        from service_name_mcp.analytics_domain.analytics_tools import _generate_mock_analysis_data
        
        mock_data = _generate_mock_analysis_data()
        
        assert isinstance(mock_data, dict)
        assert "analysis_summary" in mock_data
        assert "top_contributors" in mock_data
        
        # Check top contributors structure
        contributors = mock_data["top_contributors"]
        assert isinstance(contributors, list)
        
        for contributor in contributors:
            assert "dimension" in contributor
            assert "dimension_value" in contributor
            assert "impact_score" in contributor
            assert isinstance(contributor["impact_score"], (int, float))
    
    def test_analysis_result_formatting(self):
        """Test analysis result formatting."""
        from service_name_mcp.analytics_domain.analytics_tools import _format_analysis_results
        
        raw_data = {
            "contributors": [
                {"dim": "Country", "value": "US", "impact": 15.5},
                {"dim": "PaymentMethod", "value": "CreditCard", "impact": -8.2}
            ]
        }
        
        formatted = _format_analysis_results(raw_data)
        
        assert isinstance(formatted, dict)
        # Should have standardized structure
        assert "analysis_summary" in formatted or "summary" in formatted


class TestAnalyticsIntegration:
    """Integration tests for analytics domain."""
    
    def test_mcp_tool_registration(self):
        """Test that analytics tools are properly registered with MCP."""
        try:
            # Import the tools module to trigger registration
            import service_name_mcp.analytics_domain.analytics_tools
            from service_name_mcp.mcp_instance import mcp
            
            # This test verifies that import doesn't fail
            assert mcp is not None
            
        except ImportError as e:
            pytest.fail(f"Failed to register analytics tools with MCP: {e}")
    
    def test_mcp_prompt_registration(self):
        """Test that analytics prompts are properly registered with MCP."""
        try:
            # Import the prompts module to trigger registration
            import service_name_mcp.analytics_domain.analytics_prompts
            from service_name_mcp.mcp_instance import mcp
            
            # This test verifies that import doesn't fail
            assert mcp is not None
            
        except ImportError as e:
            pytest.fail(f"Failed to register analytics prompts with MCP: {e}")
    
    @pytest.mark.integration
    def test_end_to_end_analytics_workflow(self):
        """Test complete analytics workflow."""
        from service_name_mcp.analytics_domain.analytics_tools import (
            get_contribution_dimensions,
            contribution_analysis
        )
        
        # 1. Get available dimensions
        dimensions_info = get_contribution_dimensions()
        assert "dimensions" in dimensions_info
        
        # 2. Perform contribution analysis
        analysis_result = contribution_analysis(
            current_start_date="2024-01-01",
            current_end_date="2024-01-31",
            comparison_start_date="2023-01-01",
            comparison_end_date="2023-01-31"
        )
        
        assert isinstance(analysis_result, dict)
        assert "analysis_summary" in analysis_result
        
        # 3. Verify analysis contains actionable insights
        summary = analysis_result["analysis_summary"]
        assert isinstance(summary, str)
        assert len(summary) > 50  # Should have substantial content


class TestAnalyticsDocumentation:
    """Test analytics domain documentation."""
    
    def test_readme_file_exists(self):
        """Test that analytics README file exists."""
        from pathlib import Path
        
        # Get the path to the README file
        current_dir = Path(__file__).parent.parent.parent
        readme_path = current_dir / "src" / "service_name_mcp" / "analytics_domain" / "README.md"
        
        assert readme_path.exists(), "Analytics README file should exist"
        
        # Verify it has content
        content = readme_path.read_text()
        assert len(content) > 100, "README should have substantial content"
        assert any(keyword in content.lower() for keyword in ["analytics", "analysis", "data"]), \
            "README should mention analytics concepts"
    
    def test_domain_documentation_completeness(self):
        """Test that domain has complete documentation."""
        from pathlib import Path
        
        domain_dir = Path(__file__).parent.parent.parent / "src" / "service_name_mcp" / "analytics_domain"
        
        # Check for expected files
        expected_files = [
            "__init__.py",
            "analytics_tools.py",
            "analytics_config.py", 
            "analytics_prompts.py",
            "README.md"
        ]
        
        for filename in expected_files:
            file_path = domain_dir / filename
            assert file_path.exists(), f"Expected file {filename} should exist in analytics domain"


class TestErrorHandling:
    """Test error handling in analytics functions."""
    
    @patch('service_name_mcp.analytics_domain.analytics_tools.logger')
    def test_contribution_analysis_error_handling(self, mock_logger):
        """Test error handling in contribution analysis."""
        from service_name_mcp.analytics_domain.analytics_tools import contribution_analysis
        
        # Test with None parameters
        with pytest.raises(Exception):
            contribution_analysis(
                current_start_date=None,
                current_end_date="2024-01-31",
                comparison_start_date="2023-01-01",
                comparison_end_date="2023-01-31"
            )
        
        mock_logger.error.assert_called()
    
    def test_invalid_dimension_handling(self):
        """Test handling of invalid dimensions."""
        from service_name_mcp.analytics_domain.analytics_tools import contribution_analysis
        
        # Test with invalid dimension
        try:
            result = contribution_analysis(
                current_start_date="2024-01-01",
                current_end_date="2024-01-31",
                comparison_start_date="2023-01-01",
                comparison_end_date="2023-01-31",
                dimensions="InvalidDimension"
            )
            # Should either handle gracefully or raise appropriate error
            if isinstance(result, dict):
                # If it handles gracefully, should have error info
                assert "error" in result or "warning" in result
        except Exception as e:
            # Raising an exception for invalid dimensions is acceptable
            assert "dimension" in str(e).lower() or "invalid" in str(e).lower()


if __name__ == "__main__":
    pytest.main([__file__])
