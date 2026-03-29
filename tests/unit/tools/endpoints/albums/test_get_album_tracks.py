from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.models.spotify import PagedResultModel

from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import SimplifiedTrackView
from spotantic_mcp.tools.endpoints.albums._get_album_tracks import get_album_tracks_tool


@pytest.mark.asyncio
async def test_get_album_tracks_tool(mock_context, example_simplified_track_data):
    mock_response = MagicMock()
    mock_response.data = PagedResultModel(
        items=[example_simplified_track_data],
        total=1,
        limit=1,
        offset=0,
        href="https://api.spotify.com/v1/albums/album123/tracks?offset=0&limit=1",  # type: ignore
    )

    with patch(
        "spotantic_mcp.tools.endpoints.albums._get_album_tracks.get_album_tracks",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await get_album_tracks_tool(ctx=mock_context, album_id="album123")
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client, album_id="album123", limit=10, offset=0, market=None
        )
        assert res == PagedResultView[SimplifiedTrackView].model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_album_tracks_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_album_tracks_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
