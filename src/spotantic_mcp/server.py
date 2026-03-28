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


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context."""

    client = await setup_spotantic_client()
    try:
        yield AppContext(client=client)
    finally:
        pass


mcp = FastMCP("Spotantic MCP", lifespan=app_lifespan)

if __name__ == "__main__":
    mcp.run()
