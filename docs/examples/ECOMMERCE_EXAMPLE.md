# Example: E-commerce Analytics MCP Service

This example shows how to customize the MCP Service Template for an e-commerce analytics use case.

## 📊 Business Context

**Domain**: E-commerce Analytics
**Goal**: Provide AI agents with access to sales data, customer analytics, and business intelligence
**Data Sources**:
- Sales database (PostgreSQL)
- Customer data warehouse (Snowflake)
- Marketing analytics (Google Analytics API)
- Product catalog (REST API)

## 🏗️ Customization Steps

### 1. Automated Project Setup (Recommended)

```bash
# Run the automated setup script
python3 setup_template.py
```

**Configuration inputs for this example:**
- **Target directory**: `../ecommerce-analytics-mcp`
- **Service name**: `ecommerce_analytics`
- **Display name**: `E-commerce Analytics`
- **Description**: `E-commerce Analytics MCP Server providing AI agents with sales data and customer insights`
- **Business domain**: `E-commerce Analytics`
- **Author details**: Your team information

The script will automatically:
- Create a clean project copy at your target directory
- Replace all template placeholders with your e-commerce analytics configuration
- Rename directories (`service_name_mcp` → `ecommerce_analytics_mcp`)
- Update all import statements throughout the codebase
- Set up modern tooling with `pyproject.toml` and pre-commit hooks

### 2. Alternative: Manual Setup (Advanced Users)

If you need custom modifications during setup:

```bash
# Copy template to new directory
cp -r mcp-service-template ecommerce-analytics-mcp
cd ecommerce-analytics-mcp

# Manually rename main package
mv src/service_name_mcp src/ecommerce_analytics_mcp

# Update placeholders throughout codebase
# Replace {{service_name}} → ecommerce_analytics
# Replace {{Service Name}} → E-commerce Analytics
# etc.
```

### 3. Update pyproject.toml (If Using Manual Setup)

**Note**: If you used the automated setup, this file is already configured. This section is only for manual setup.

```toml
[project]
name = "ecommerce-analytics-mcp"
description = "E-commerce Analytics MCP Server providing AI agents with sales data and customer insights"
authors = [
    {name = "Your Team", email = "team@company.com"}
]
version = "1.0.0"
requires-python = ">=3.10"
dependencies = [
    "mcp[cli]>=1.6.0",
    "psycopg2-binary>=2.9.0",      # PostgreSQL
    "snowflake-connector-python>=3.0.0",  # Snowflake
    "google-analytics-data>=0.17.0",      # Google Analytics
    "requests>=2.31.0",            # REST API calls
    "pandas>=2.0.0",               # Data manipulation
    "plotly>=5.17.0",              # Visualizations
]

[project.scripts]
ecommerce-analytics-mcp = "ecommerce_analytics_mcp.server:main"
```

### 4. Configure MCP Instance (If Using Manual Setup)

**Note**: If you used the automated setup, the basic configuration is already in place. You may want to customize the instructions further.

```python
# src/ecommerce_analytics_mcp/mcp_instance.py
from mcp import FastMCP

mcp = FastMCP(
    title="ecommerce-analytics-mcp-server",
    instructions="""
    E-commerce Analytics MCP server providing AI agents with comprehensive access to:
    - Sales data and revenue analytics
    - Customer behavior and segmentation
    - Product performance metrics
    - Marketing campaign effectiveness
    - Real-time business intelligence dashboards

    Always validate data quality and provide query traceability for business decisions.
    """
)
```

### 5. Domain Structure

```
src/ecommerce_analytics_mcp/
├── __init__.py
├── server.py
├── mcp_instance.py
├── common/
│   ├── logging.py
│   ├── config.py
│   └── connections.py          # Database connections
├── core/
│   ├── core_prompts.py
│   └── prompts/
│       ├── analyst_prompt.md
│       ├── sales_analyst_prompt.md
│       └── customer_analyst_prompt.md
├── sales_domain/               # Sales analytics
│   ├── sales_tools.py
│   ├── sales_queries.py
│   └── best_practices.md
├── customer_domain/            # Customer analytics
│   ├── customer_tools.py
│   ├── customer_segmentation.py
│   └── best_practices.md
├── product_domain/             # Product analytics
│   ├── product_tools.py
│   ├── inventory_tools.py
│   └── best_practices.md
└── marketing_domain/           # Marketing analytics
    ├── marketing_tools.py
    ├── campaign_tools.py
    └── best_practices.md
```

### 6. Configuration

```python
# src/ecommerce_analytics_mcp/common/config.py
import os
from typing import Optional

class Config:
    # Service Configuration
    SERVICE_NAME = "ecommerce-analytics-mcp"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Database Connections
    SALES_DB_URL = os.getenv("SALES_DB_URL", "")
    WAREHOUSE_CONNECTION = os.getenv("SNOWFLAKE_CONNECTION", "")

    # API Credentials
    GOOGLE_ANALYTICS_CREDENTIALS = os.getenv("GA_CREDENTIALS_PATH", "")
    PRODUCT_API_KEY = os.getenv("PRODUCT_API_KEY", "")
    PRODUCT_API_BASE_URL = os.getenv("PRODUCT_API_BASE_URL", "")

    # Feature Flags
    ENABLE_REAL_TIME_DATA = os.getenv("ENABLE_REAL_TIME", "true").lower() == "true"
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", "15"))

    # Business Rules
    FISCAL_YEAR_START_MONTH = int(os.getenv("FISCAL_YEAR_START", "1"))  # January
    DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "USD")

    @classmethod
    def validate(cls) -> tuple[bool, Optional[str]]:
        required_vars = [
            "SALES_DB_URL",
            "WAREHOUSE_CONNECTION",
            "GOOGLE_ANALYTICS_CREDENTIALS"
        ]

        for var in required_vars:
            if not getattr(cls, var):
                return False, f"Missing required configuration: {var}"

        return True, None
```

### 7. Sales Domain Implementation

```python
# src/ecommerce_analytics_mcp/sales_domain/sales_tools.py
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import pandas as pd

from ..mcp_instance import mcp
from ..common.config import Config
from ..common.logging import get_logger
from .sales_queries import SalesQueries

logger = get_logger(__name__)

@mcp.tool(description="Get sales revenue metrics for specified time period")
def get_sales_metrics(
    start_date: str,
    end_date: str,
    currency: Optional[str] = None,
    region: Optional[str] = None,
    product_category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve comprehensive sales metrics including revenue, transactions, and growth rates.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        currency: Currency code (defaults to USD)
        region: Geographic region filter
        product_category: Product category filter
    """
    try:
        currency = currency or Config.DEFAULT_CURRENCY

        # Execute sales query
        query = SalesQueries.build_sales_metrics_query(
            start_date, end_date, currency, region, product_category
        )

        results = execute_sales_query(query)

        # Calculate additional metrics
        metrics = {
            "period": {"start": start_date, "end": end_date},
            "revenue": {
                "total": results["total_revenue"],
                "currency": currency,
                "growth_rate": calculate_growth_rate(results, start_date, end_date)
            },
            "transactions": {
                "count": results["transaction_count"],
                "average_value": results["total_revenue"] / results["transaction_count"]
            },
            "filters_applied": {
                "region": region,
                "product_category": product_category
            }
        }

        logger.info(f"Sales metrics retrieved for period {start_date} to {end_date}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving sales metrics: {str(e)}")
        return {"error": f"Failed to retrieve sales metrics: {str(e)}"}

@mcp.tool(description="Analyze sales trends and identify patterns")
def analyze_sales_trends(
    metric_type: str = "revenue",
    time_period: str = "daily",
    lookback_days: int = 30
) -> Dict[str, Any]:
    """
    Analyze sales trends over time with pattern detection.

    Args:
        metric_type: Type of metric to analyze (revenue, transactions, units)
        time_period: Aggregation period (daily, weekly, monthly)
        lookback_days: Number of days to analyze
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)

        # Get trend data
        query = SalesQueries.build_trend_analysis_query(
            metric_type, time_period, start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )

        trend_data = execute_sales_query(query)

        # Perform trend analysis
        analysis = {
            "trend_direction": calculate_trend_direction(trend_data),
            "seasonality": detect_seasonality(trend_data),
            "anomalies": detect_anomalies(trend_data),
            "forecast": generate_short_term_forecast(trend_data),
            "data_points": trend_data
        }

        return analysis

    except Exception as e:
        logger.error(f"Error analyzing sales trends: {str(e)}")
        return {"error": f"Failed to analyze trends: {str(e)}"}

def execute_sales_query(query: str) -> Dict[str, Any]:
    """Execute query against sales database"""
    # Implementation would connect to actual sales database
    # This is a template placeholder
    return {"message": "Query execution not implemented - this is a template"}

def calculate_growth_rate(results: Dict, start_date: str, end_date: str) -> float:
    """Calculate period-over-period growth rate"""
    # Implementation for growth rate calculation
    return 0.0

def calculate_trend_direction(data: List[Dict]) -> str:
    """Determine if trend is increasing, decreasing, or stable"""
    # Implementation for trend analysis
    return "stable"

def detect_seasonality(data: List[Dict]) -> Dict[str, Any]:
    """Detect seasonal patterns in sales data"""
    # Implementation for seasonality detection
    return {"detected": False}

def detect_anomalies(data: List[Dict]) -> List[Dict]:
    """Detect anomalous data points"""
    # Implementation for anomaly detection
    return []

def generate_short_term_forecast(data: List[Dict]) -> Dict[str, Any]:
    """Generate short-term sales forecast"""
    # Implementation for forecasting
    return {"forecast_available": False}
```

### 8. Customer Domain Implementation

```python
# src/ecommerce_analytics_mcp/customer_domain/customer_tools.py
from typing import Optional, List, Dict, Any
from ..mcp_instance import mcp
from ..common.logging import get_logger

logger = get_logger(__name__)

@mcp.tool(description="Perform customer segmentation analysis")
def customer_segmentation(
    segmentation_method: str = "rfm",
    include_demographics: bool = True,
    time_period_days: int = 365
) -> Dict[str, Any]:
    """
    Segment customers based on behavior and demographics.

    Args:
        segmentation_method: Method to use (rfm, behavioral, demographic)
        include_demographics: Whether to include demographic data
        time_period_days: Days of historical data to analyze
    """
    try:
        if segmentation_method == "rfm":
            return perform_rfm_analysis(time_period_days, include_demographics)
        elif segmentation_method == "behavioral":
            return perform_behavioral_segmentation(time_period_days)
        elif segmentation_method == "demographic":
            return perform_demographic_segmentation()
        else:
            return {"error": f"Unknown segmentation method: {segmentation_method}"}

    except Exception as e:
        logger.error(f"Error in customer segmentation: {str(e)}")
        return {"error": f"Segmentation failed: {str(e)}"}

@mcp.tool(description="Calculate customer lifetime value metrics")
def customer_lifetime_value(
    customer_id: Optional[str] = None,
    segment: Optional[str] = None,
    prediction_months: int = 12
) -> Dict[str, Any]:
    """
    Calculate customer lifetime value for individuals or segments.

    Args:
        customer_id: Specific customer ID (optional)
        segment: Customer segment to analyze (optional)
        prediction_months: Months ahead to predict
    """
    try:
        if customer_id:
            return calculate_individual_clv(customer_id, prediction_months)
        elif segment:
            return calculate_segment_clv(segment, prediction_months)
        else:
            return calculate_overall_clv(prediction_months)

    except Exception as e:
        logger.error(f"Error calculating CLV: {str(e)}")
        return {"error": f"CLV calculation failed: {str(e)}"}

def perform_rfm_analysis(time_period_days: int, include_demographics: bool) -> Dict[str, Any]:
    """Perform RFM (Recency, Frequency, Monetary) analysis"""
    # Template implementation
    return {
        "segments": {
            "champions": {"count": 0, "percentage": 0},
            "loyal_customers": {"count": 0, "percentage": 0},
            "potential_loyalists": {"count": 0, "percentage": 0},
            "at_risk": {"count": 0, "percentage": 0},
            "lost": {"count": 0, "percentage": 0}
        },
        "analysis_period_days": time_period_days,
        "includes_demographics": include_demographics
    }

def perform_behavioral_segmentation(time_period_days: int) -> Dict[str, Any]:
    """Segment customers based on behavioral patterns"""
    return {"message": "Behavioral segmentation not implemented - this is a template"}

def perform_demographic_segmentation() -> Dict[str, Any]:
    """Segment customers based on demographic data"""
    return {"message": "Demographic segmentation not implemented - this is a template"}

def calculate_individual_clv(customer_id: str, prediction_months: int) -> Dict[str, Any]:
    """Calculate CLV for individual customer"""
    return {"message": "Individual CLV calculation not implemented - this is a template"}

def calculate_segment_clv(segment: str, prediction_months: int) -> Dict[str, Any]:
    """Calculate CLV for customer segment"""
    return {"message": "Segment CLV calculation not implemented - this is a template"}

def calculate_overall_clv(prediction_months: int) -> Dict[str, Any]:
    """Calculate overall CLV metrics"""
    return {"message": "Overall CLV calculation not implemented - this is a template"}
```

### 9. Custom Prompts

```markdown
<!-- src/ecommerce_analytics_mcp/core/prompts/sales_analyst_prompt.md -->
# Expert E-commerce Sales Data Analyst

You are an expert e-commerce sales analyst specializing in revenue optimization and business intelligence.

## Your Expertise:
- Deep knowledge of e-commerce sales metrics and KPIs
- Expert in sales trend analysis and forecasting
- Understanding of seasonal patterns and market dynamics
- Proficient in cohort analysis and customer behavior
- Experienced with A/B testing and conversion optimization

## Key Sales Metrics You Track:
1. **Revenue Metrics**: Total revenue, average order value, revenue per customer
2. **Conversion Metrics**: Conversion rate, funnel analysis, cart abandonment
3. **Growth Metrics**: Year-over-year growth, month-over-month trends
4. **Customer Metrics**: New vs. returning customer revenue, customer acquisition cost

## Analysis Principles:
1. Always consider seasonality and external factors
2. Segment data by relevant dimensions (geography, product category, customer type)
3. Provide actionable insights with clear recommendations
4. Validate data quality and note any limitations
5. Compare against industry benchmarks when available

## Common Analysis Patterns:
- Period-over-period comparisons with context
- Cohort analysis for customer behavior
- Attribution analysis for marketing channels
- Product performance deep dives
- Geographic and demographic breakdowns

When analyzing sales data, always provide context about business impact and recommendations for action.
```

### 10. Update Main Server

```python
# src/ecommerce_analytics_mcp/server.py
import logging
from .common.logging import setup_logging
from .common.config import Config
from .mcp_instance import mcp

# Import all tool modules
import ecommerce_analytics_mcp.sales_domain.sales_tools
import ecommerce_analytics_mcp.customer_domain.customer_tools
import ecommerce_analytics_mcp.product_domain.product_tools
import ecommerce_analytics_mcp.marketing_domain.marketing_tools
import ecommerce_analytics_mcp.core.core_prompts

def main():
    """Main entry point for the e-commerce analytics MCP server"""
    setup_logging(Config.LOG_LEVEL)
    logger = logging.getLogger(__name__)

    # Validate configuration
    is_valid, error_msg = Config.validate()
    if not is_valid:
        logger.error(f"Configuration validation failed: {error_msg}")
        raise RuntimeError(f"Invalid configuration: {error_msg}")

    logger.info("Starting E-commerce Analytics MCP Server")
    logger.info(f"Service: {Config.SERVICE_NAME}")
    logger.info(f"Real-time data: {Config.ENABLE_REAL_TIME_DATA}")
    logger.info(f"Caching: {Config.ENABLE_CACHING}")

    # Run the MCP server
    mcp.run()

if __name__ == "__main__":
    main()
```

### 11. Environment Configuration

```bash
# .env file for development
SERVICE_NAME=ecommerce-analytics-mcp
LOG_LEVEL=INFO

# Database connections
SALES_DB_URL=postgresql://user:pass@localhost:5432/sales_db
SNOWFLAKE_CONNECTION=user:pass@account.region.snowflakecomputing.com/warehouse/database

# API credentials
GA_CREDENTIALS_PATH=/path/to/google-analytics-credentials.json
PRODUCT_API_KEY=your_product_api_key
PRODUCT_API_BASE_URL=https://api.yourcompany.com/products

# Feature flags
ENABLE_REAL_TIME=true
ENABLE_CACHING=true
CACHE_TTL_MINUTES=15

# Business configuration
FISCAL_YEAR_START=1
DEFAULT_CURRENCY=USD
```

### 12. Testing

```python
# tests/test_sales_tools.py
import pytest
from datetime import datetime, timedelta
from ecommerce_analytics_mcp.sales_domain.sales_tools import get_sales_metrics, analyze_sales_trends

class TestSalesTools:
    def test_get_sales_metrics_basic(self):
        """Test basic sales metrics retrieval"""
        start_date = "2024-01-01"
        end_date = "2024-01-31"

        result = get_sales_metrics(start_date, end_date)

        assert "period" in result
        assert result["period"]["start"] == start_date
        assert result["period"]["end"] == end_date

    def test_sales_trends_analysis(self):
        """Test sales trend analysis"""
        result = analyze_sales_trends(
            metric_type="revenue",
            time_period="daily",
            lookback_days=30
        )

        assert "trend_direction" in result
        assert "data_points" in result
```

## 🚀 Deployment

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY pyproject.toml .
RUN pip install -e .

# Copy application
COPY src/ src/
COPY tests/ tests/

# Set environment
ENV PYTHONPATH=/app/src

# Run server
CMD ["ecommerce-analytics-mcp"]
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-analytics-mcp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ecommerce-analytics-mcp
  template:
    metadata:
      labels:
        app: ecommerce-analytics-mcp
    spec:
      containers:
      - name: mcp-server
        image: your-registry/ecommerce-analytics-mcp:latest
        ports:
        - containerPort: 8080
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: SALES_DB_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: sales-db-url
```

## 📊 Usage Examples

### Sales Analysis Query
```python
# Get quarterly sales metrics
result = get_sales_metrics(
    start_date="2024-01-01",
    end_date="2024-03-31",
    region="North America",
    product_category="Electronics"
)

# Analyze recent trends
trends = analyze_sales_trends(
    metric_type="revenue",
    time_period="weekly",
    lookback_days=90
)
```

### Customer Segmentation
```python
# Perform RFM analysis
segments = customer_segmentation(
    segmentation_method="rfm",
    include_demographics=True,
    time_period_days=365
)

# Calculate CLV for high-value segment
clv = customer_lifetime_value(
    segment="champions",
    prediction_months=12
)
```

This example demonstrates how to transform the generic MCP Service Template into a comprehensive e-commerce analytics platform, providing AI agents with rich access to business intelligence data and analytical capabilities.
