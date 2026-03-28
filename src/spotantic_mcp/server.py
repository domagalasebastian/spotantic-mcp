from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP
from spotantic.client import SpotanticClient

from spotantic_mcp._setup_spotantic_client import setup_spotantic_client


@dataclass
class AppContext:
    """Application context for the Spotantic MCP server."""

    client: SpotanticClient
    """The initialized Spotantic client instance."""


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context.

    This function initializes the Spotantic client and yields an application context.

    Args:
        server: The MCP server instance.

    Yields:
        An instance of AppContext containing the initialized Spotantic client.
    """

    client = await setup_spotantic_client()
    yield AppContext(client=client)


def main() -> None:
    """Entry point for the Spotantic MCP server."""
    mcp = FastMCP("Spotantic MCP", lifespan=app_lifespan)
    mcp.run()


if __name__ == "__main__":
    main()
