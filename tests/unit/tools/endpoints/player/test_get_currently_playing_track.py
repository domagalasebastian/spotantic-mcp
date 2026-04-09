from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.types import SpotifyItemType

from spotantic_mcp.tools.endpoints._views import CurrentlyPlayingItemView
from spotantic_mcp.tools.endpoints.player._get_currently_playing_track import get_currently_playing_track_tool


@pytest.mark.asyncio
async def test_get_currently_playing_track_tool(mock_context, example_currently_playing_item_data):
    mock_response = MagicMock()
    mock_response.data = example_currently_playing_item_data

    with patch(
        "spotantic_mcp.tools.endpoints.player._get_currently_playing_track.get_currently_playing_track",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        additional_types = (SpotifyItemType.TRACK, SpotifyItemType.EPISODE)
        res = await get_currently_playing_track_tool(ctx=mock_context, market=None)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            additional_types=additional_types,
            market=None,
        )
        assert res == CurrentlyPlayingItemView.model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_currently_playing_track_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_currently_playing_track_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
