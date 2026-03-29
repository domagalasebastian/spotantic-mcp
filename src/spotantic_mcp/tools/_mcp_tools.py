from spotantic_mcp.tools._tool_group import ToolGroup

from .endpoints import endpoint_tools

spotantic_mcp_tools = ToolGroup(
    name="Spotantic MCP Tools",
    tools=[
        endpoint_tools,
    ],
)
