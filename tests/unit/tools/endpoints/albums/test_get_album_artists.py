from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints._views import SimplifiedArtistView
from spotantic_mcp.tools.endpoints.albums._get_album_artists import get_album_artists_tool


@pytest.mark.asyncio
async def test_get_album_artists_tool(mock_context, example_album_data):
    mock_response = MagicMock()
    mock_response.data = example_album_data

    with patch(
        "spotantic_mcp.tools.endpoints.albums._get_album_artists.get_album", new=AsyncMock(return_value=mock_response)
    ) as mock_api_call:
        res = await get_album_artists_tool(ctx=mock_context, album_id=example_album_data.album_id)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client, album_id=example_album_data.album_id, market=None
        )
        assert res == [SimplifiedArtistView.model_validate(artist_data) for artist_data in example_album_data.artists]


@pytest.mark.asyncio
async def test_get_album_artists_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_album_artists_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
