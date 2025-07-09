import sys
from service_name_mcp import __version__
from service_name_mcp.common.logging import logger
from service_name_mcp.mcp_instance import mcp

# Import tool modules to register them with the MCP server
# The @mcp.tool and @mcp.prompt decorators will execute during import, registering tools
# TODO: Replace these with your actual domain modules
import service_name_mcp.sqlite_domain.sqlite_tools
import service_name_mcp.rest_api_domain.rest_api_tools  
import service_name_mcp.file_processing_domain.file_processing_tools
import service_name_mcp.core.core_prompts
import service_name_mcp.analytics_domain.analytics_tools
import service_name_mcp.analytics_domain.analytics_prompts
import service_name_mcp.docs_domain.docs_tools

def main() -> None:
    # writing to stderr because stdout is used for the transport
    # and we want to see the logs in the console
    logger.error("Starting {{service_name}} MCP server")
    logger.error(f"Version: {__version__}")
    logger.error(f"Python version: {sys.version}")
    logger.error(f"Platform: {sys.platform}")

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
