from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints._views import SimplifiedArtistView
from spotantic_mcp.tools.endpoints.artists._get_several_artists import get_several_artists_tool


@pytest.mark.asyncio
async def test_get_several_artists_tool(mock_context, example_simplified_artist_data):
    mock_response = MagicMock()
    mock_response.data = [example_simplified_artist_data]

    with patch(
        "spotantic_mcp.tools.endpoints.artists._get_several_artists.get_several_artists",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await get_several_artists_tool(
            ctx=mock_context,
            artist_ids=["artist123"],
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            artist_ids=["artist123"],
        )
        assert res == [SimplifiedArtistView.model_validate(artist) for artist in mock_response.data]


@pytest.mark.asyncio
async def test_get_several_artists_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_several_artists_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
