from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints._views import PlaylistTrackView
from spotantic_mcp.tools.utilities._get_all_playlist_items_tool import get_all_playlist_items_tool


@pytest.mark.asyncio
async def test_get_all_playlist_items_tool(mock_context, example_playlist_track_data):
    with patch(
        "spotantic_mcp.tools.utilities._get_all_playlist_items_tool.get_all_playlist_items",
        new=AsyncMock(return_value=[example_playlist_track_data]),
    ) as mock_script_call:
        res = await get_all_playlist_items_tool(
            ctx=mock_context,
            playlist_id="playlist-id",
            fields="field1,field2",
            market="US",
        )

    mock_script_call.assert_awaited_once_with(
        mock_context.request_context.lifespan_context.client,
        playlist_id="playlist-id",
        fields="field1,field2",
        market="US",
    )
    assert res == [PlaylistTrackView.model_validate(example_playlist_track_data)]


@pytest.mark.asyncio
async def test_get_all_playlist_items_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_all_playlist_items_tool"]
    assert len(matching_tools) == 1
    assert matching_tools[0].outputSchema is not None
