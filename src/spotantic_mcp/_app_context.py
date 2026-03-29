from dataclasses import dataclass

from spotantic.client import SpotanticClient


@dataclass
class AppContext:
    """Application context for the Spotantic MCP server."""

    client: SpotanticClient
    """The initialized Spotantic client instance."""
