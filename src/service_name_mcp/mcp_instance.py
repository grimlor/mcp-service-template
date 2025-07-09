from mcp.server.fastmcp import FastMCP

# Create the FastMCP server instance
# Customize the title and instructions for your specific service domain
mcp = FastMCP(
    title="{{service_name}}-mcp-server",
    instructions="{{Service Description}} MCP server providing AI agents with access to {{domain}} data and functionality",
)
