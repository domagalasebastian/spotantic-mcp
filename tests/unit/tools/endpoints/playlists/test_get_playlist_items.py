from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.models.spotify import PagedResultModel
from spotantic.types import SpotifyItemType

from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import PlaylistTrackView
from spotantic_mcp.tools.endpoints.playlists._get_playlist_items import get_playlist_items_tool


@pytest.mark.asyncio
async def test_get_playlist_items_tool(mock_context, example_playlist_track_data):
    mock_response = MagicMock()
    mock_response.data = PagedResultModel(
        items=[example_playlist_track_data],
        total=1,
        limit=1,
        offset=0,
        href="https://api.spotify.com/v1/browse/playlists?offset=0&limit=1",  # type: ignore
    )

    with patch(
        "spotantic_mcp.tools.endpoints.playlists._get_playlist_items.get_playlist_items",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        playlist_id = "playlistID"
        fields = None
        limit = 10
        offset = 0
        additional_types = (SpotifyItemType.TRACK, SpotifyItemType.EPISODE)
        market = None
        res = await get_playlist_items_tool(
            ctx=mock_context,
            playlist_id=playlist_id,
            fields=fields,
            limit=limit,
            offset=offset,
            market=market,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            playlist_id=playlist_id,
            fields=fields,
            limit=limit,
            additional_types=additional_types,
            offset=offset,
            market=market,
        )
        assert res == PagedResultView[PlaylistTrackView].model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_playlist_items_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_playlist_items_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
