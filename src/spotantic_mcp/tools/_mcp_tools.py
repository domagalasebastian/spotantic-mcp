from spotantic_mcp.tools._tool_group import ToolGroup

from .endpoints import endpoint_tools
from .utilities import utility_tools

spotantic_mcp_tools = ToolGroup(
    name="Spotantic MCP Tools",
    tools=[
        endpoint_tools,
        utility_tools,
    ],
)
