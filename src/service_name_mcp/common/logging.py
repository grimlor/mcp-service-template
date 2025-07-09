import logging
import sys

# Create logger for the service
# Replace 'service_name' with your actual service name
logger = logging.getLogger("{{service_name}}-mcp")

# Configure logging to stderr (stdout is used for MCP transport)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)  # Change to DEBUG for more verbose logging


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a logger instance for the given name.

    Args:
        name: Optional logger name. If not provided, returns the default service logger.

    Returns:
        Configured logger instance.
    """
    if name:
        return logging.getLogger(f"{{service_name}}-mcp.{name}")
    return logger
