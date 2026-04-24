from types import SimpleNamespace
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.playlists._add_items_to_playlist import add_items_to_playlist_tool


@pytest.mark.asyncio
async def test_add_items_to_playlist_tool(mock_context):
    snapshot_id = "snapshotID"
    mock_response = MagicMock()
    mock_response.data = SimpleNamespace(snapshot_id="snapshotID")

    with patch(
        "spotantic_mcp.tools.endpoints.playlists._add_items_to_playlist.add_items_to_playlist",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        playlist_id = "playlistID"
        uris = ["uri1"]
        position = 2
        res = await add_items_to_playlist_tool(
            ctx=mock_context,
            playlist_id=playlist_id,
            uris=uris,
            position=position,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            playlist_id=playlist_id,
            uris=uris,
            position=position,
        )
        assert res == snapshot_id


@pytest.mark.asyncio
async def test_add_items_to_playlist_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "add_items_to_playlist_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
