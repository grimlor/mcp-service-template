"""
Analytics Configuration for {{Service Name}} MCP Server

This module contains configuration for analytics tools, including
default metrics, dimensions, and analysis parameters.
"""

from typing import Any

# Default metrics configuration
DEFAULT_METRICS = {
    "success_rate": {
        "description": "Percentage of successful operations",
        "format": "percentage",
        "default_threshold": 90.0,
    },
    "volume_count": {
        "description": "Total volume of operations",
        "format": "integer",
        "default_threshold": 1000,
    },
    "average_duration": {
        "description": "Average processing time",
        "format": "decimal",
        "default_threshold": 5.0,
    },
    "error_rate": {
        "description": "Percentage of failed operations",
        "format": "percentage",
        "default_threshold": 5.0,
    },
}

# Dimension configuration
DIMENSION_CONFIG = {
    "business_dimensions": ["Category", "Product", "Service", "Type"],
    "geographic_dimensions": ["Region", "Country", "City", "Zone"],
    "temporal_dimensions": ["Quarter", "Month", "Week", "DayOfWeek", "Hour"],
    "operational_dimensions": ["Channel", "Source", "Method", "Status"],
}

# Analysis parameters
ANALYSIS_CONFIG = {
    "default_min_volume": 100,
    "confidence_level": 0.95,
    "significance_threshold": 0.05,
    "max_dimensions": 10,
    "default_time_window_days": 30,
}

# Query configuration
QUERY_CONFIG = {
    "default_database": "DefaultDB",
    "timeout_seconds": 300,
    "max_rows": 50000,
    "query_base_url": "https://your-query-platform.com",
}


def get_default_metric() -> str:
    """Get the default metric for analytics operations."""
    return "success_rate"


def get_available_metrics() -> dict[str, Any]:
    """Get all available metrics and their configuration."""
    return DEFAULT_METRICS


def get_dimension_categories() -> dict[str, list[str]]:
    """Get dimension categories and their associated dimensions."""
    return DIMENSION_CONFIG


def validate_metric(metric: str) -> bool:
    """Validate if a metric is supported."""
    return metric in DEFAULT_METRICS


def validate_dimension(dimension: str) -> bool:
    """Validate if a dimension is supported."""
    all_dimensions = []
    for dims in DIMENSION_CONFIG.values():
        all_dimensions.extend(dims)
    return dimension in all_dimensions
