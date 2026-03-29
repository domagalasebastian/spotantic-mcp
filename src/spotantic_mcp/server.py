from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP

from spotantic_mcp._app_context import AppContext
from spotantic_mcp._spotantic_client import create_spotantic_client


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


def main() -> None:
    """Entry point for the Spotantic MCP server."""
    mcp = FastMCP("Spotantic MCP", lifespan=app_lifespan)
    mcp.run()


if __name__ == "__main__":
    main()
