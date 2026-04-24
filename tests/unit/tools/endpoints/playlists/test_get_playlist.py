from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.types import SpotifyItemType

from spotantic_mcp.tools.endpoints._views import PlaylistBaseView
from spotantic_mcp.tools.endpoints.playlists._get_playlist import get_playlist_tool


@pytest.mark.asyncio
async def test_get_playlist_tool(mock_context, example_playlist_data):
    mock_response = MagicMock()
    mock_response.data = example_playlist_data

    with patch(
        "spotantic_mcp.tools.endpoints.playlists._get_playlist.get_playlist",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        playlist_id = "playlistID"
        fields = None
        additional_types = (SpotifyItemType.TRACK, SpotifyItemType.EPISODE)
        market = None
        res = await get_playlist_tool(
            ctx=mock_context,
            playlist_id=playlist_id,
            market=market,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            playlist_id=playlist_id,
            fields=fields,
            additional_types=additional_types,
            market=market,
        )
        assert res == PlaylistBaseView.model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_playlist_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_playlist_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
