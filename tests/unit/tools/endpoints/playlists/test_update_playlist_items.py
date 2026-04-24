from types import SimpleNamespace
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.playlists._update_playlist_items import update_playlist_items_tool


@pytest.mark.asyncio
async def test_update_playlist_items_tool(mock_context):
    snapshot_id = "snapshotID"
    mock_response = MagicMock()
    mock_response.data = SimpleNamespace(snapshot_id="snapshotID")

    with patch(
        "spotantic_mcp.tools.endpoints.playlists._update_playlist_items.update_playlist_items",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        playlist_id = "playlistID"
        uris = ["uri1"]
        range_start = 0
        insert_before = 0
        range_length = 1
        snapshot_in = "snapshotID_in"
        res = await update_playlist_items_tool(
            ctx=mock_context,
            playlist_id=playlist_id,
            uris=uris,
            range_start=range_start,
            insert_before=insert_before,
            range_length=range_length,
            snapshot_id=snapshot_in,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            playlist_id=playlist_id,
            uris=uris,
            range_start=range_start,
            insert_before=insert_before,
            range_length=range_length,
            snapshot_id=snapshot_in,
        )
        assert res == snapshot_id


@pytest.mark.asyncio
async def test_update_playlist_items_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "update_playlist_items_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
