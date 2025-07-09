import os

# Optional is imported for type hints in comments/examples


class Config:
    """
    Configuration management for the MCP service.

    This class centralizes configuration management using environment variables
    with sensible defaults. Customize this for your specific service needs.
    """

    # Service identification
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "{{service_name}}")
    SERVICE_VERSION: str = os.getenv("SERVICE_VERSION", "0.1.0")

    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Database/Data Source Configuration
    # Uncomment and customize based on your data sources:

    # SQLite Database
    # DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///data.db")

    # External APIs
    # API_BASE_URL: str = os.getenv("API_BASE_URL", "")
    # API_KEY: str = os.getenv("API_KEY", "")
    # API_SECRET: str = os.getenv("API_SECRET", "")

    # Authentication (customize for your auth provider)
    # AUTH_TOKEN: str = os.getenv("AUTH_TOKEN", "")
    # CLIENT_ID: str = os.getenv("CLIENT_ID", "")
    # CLIENT_SECRET: str = os.getenv("CLIENT_SECRET", "")

    # Documentation/Repository
    # DOCS_REPOSITORY_URL: str = os.getenv("DOCS_REPOSITORY_URL", "")
    # DOCS_ACCESS_TOKEN: str = os.getenv("DOCS_ACCESS_TOKEN", "")
    # DOCS_ORGANIZATION: str = os.getenv("DOCS_ORGANIZATION", "")
    # DOCS_PROJECT: str = os.getenv("DOCS_PROJECT", "")

    # Feature flags
    ENABLE_CACHING: bool = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "true").lower() == "true"

    # Performance settings
    MAX_QUERY_TIMEOUT: int = int(os.getenv("MAX_QUERY_TIMEOUT", "300"))  # seconds
    MAX_RESULTS_PER_QUERY: int = int(os.getenv("MAX_RESULTS_PER_QUERY", "10000"))

    @classmethod
    def validate(cls) -> None:
        """
        Validate that required configuration is present.

        Raises:
            ValueError: If required configuration is missing
        """
        required_configs = [
            # Add your required configuration keys here
            # ("DATABASE_URL", cls.DATABASE_URL),
            # ("API_KEY", cls.API_KEY),
        ]

        missing_configs = []
        for name, value in required_configs:
            if not value:
                missing_configs.append(name)

        if missing_configs:
            raise ValueError(f"Missing required configuration: {', '.join(missing_configs)}")

    @classmethod
    def get_connection_string(cls, service_type: str) -> str:
        """
        Get connection string for a specific service type.

        Args:
            service_type: Type of service ('database', 'api', etc.)

        Returns:
            Connection string for the service
        """
        # Implement your connection string logic here
        # Example:
        # if service_type == "database":
        #     return cls.DATABASE_URL
        # elif service_type == "api":
        #     return f"{cls.API_BASE_URL}/v1"

        raise NotImplementedError(f"Connection string for {service_type} not implemented")


# Global configuration instance
config = Config()
