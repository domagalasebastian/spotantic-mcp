from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP

from spotantic_mcp._app_context import AppContext
from spotantic_mcp._spotantic_client import create_spotantic_client
from spotantic_mcp.tools import ToolGroup
from spotantic_mcp.tools import spotantic_mcp_tools


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context.

    This function initializes the Spotantic client and yields an application context.

    Args:
        server: The MCP server instance.

    Yields:
        An instance of AppContext containing the initialized Spotantic client.
    """
    client = await create_spotantic_client()
    yield AppContext(client=client)


def register_tools(mcp: FastMCP, tools: ToolGroup) -> None:
    """Register tools with the MCP server.

    Args:
        mcp: The MCP server instance to register tools with.
        tools: The ToolGroup containing the tools to register.
    """

    def register_tool_group(tool_group: ToolGroup) -> None:
        """Recursively register tools from a ToolGroup.

        Args:
            tool_group: The ToolGroup whose tools are to be registered.
        """
        for tool in tool_group.tools:
            if isinstance(tool, ToolGroup):
                register_tool_group(tool)
            else:
                mcp.add_tool(tool)

    register_tool_group(tools)


def create_server(name: str) -> FastMCP:
    """Create and configure the MCP server.

    Args:
        name: The name of the MCP server.

    Returns:
        An instance of FastMCP configured with the application lifespan and registered tools.
    """
    mcp = FastMCP(name, lifespan=app_lifespan)
    register_tools(mcp, spotantic_mcp_tools)
    return mcp


def main() -> None:
    """Entry point for the Spotantic MCP server."""
    mcp = create_server("Spotantic MCP")
    mcp.run()


if __name__ == "__main__":
    main()
