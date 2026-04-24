from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.playlists._change_playlist_details import change_playlist_details_tool


@pytest.mark.asyncio
async def test_change_playlist_details_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.playlists._change_playlist_details.change_playlist_details", new=AsyncMock()
    ) as mock_api_call:
        playlist_id = "playlistID"
        name = "playlist name"
        public = True
        collaborative = True
        description = "playlist description"
        res = await change_playlist_details_tool(
            ctx=mock_context,
            playlist_id=playlist_id,
            name=name,
            public=public,
            collaborative=collaborative,
            description=description,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            playlist_id=playlist_id,
            name=name,
            public=public,
            collaborative=collaborative,
            description=description,
        )
        assert res == "Successfully changed the playlist data."


@pytest.mark.asyncio
async def test_change_playlist_details_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "change_playlist_details_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
