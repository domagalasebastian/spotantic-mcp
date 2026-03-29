import pytest
from spotantic.client import SpotanticClient

from spotantic_mcp._spotantic_client import create_spotantic_client


@pytest.mark.asyncio
async def test_spotantic_client_setup() -> None:
    """Integration test for Spotantic client setup.

    Requires valid environment variables for client credentials.
    """
    client = await create_spotantic_client()
    assert isinstance(client, SpotanticClient)
