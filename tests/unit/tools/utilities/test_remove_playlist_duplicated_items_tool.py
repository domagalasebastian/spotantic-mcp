from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.utilities._remove_playlist_duplicated_items_tool import remove_playlist_duplicated_items_tool


@pytest.mark.asyncio
async def test_remove_playlist_duplicated_items_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.utilities._remove_playlist_duplicated_items_tool.remove_playlist_duplicated_items",
        new=AsyncMock(return_value=2),
    ) as mock_script_call:
        res = await remove_playlist_duplicated_items_tool(ctx=mock_context, playlist_id="playlist-id")

    mock_script_call.assert_awaited_once_with(
        mock_context.request_context.lifespan_context.client,
        playlist_id="playlist-id",
    )
    assert res == "Removed 2 duplicated items from the playlist."


@pytest.mark.asyncio
async def test_remove_playlist_duplicated_items_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "remove_playlist_duplicated_items_tool"]
    assert len(matching_tools) == 1
    assert matching_tools[0].outputSchema is not None
