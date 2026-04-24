from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints._views import PlaylistView
from spotantic_mcp.tools.endpoints.playlists._create_playlist import create_playlist_tool


@pytest.mark.asyncio
async def test_create_playlist_tool(mock_context, example_playlist_data):
    mock_response = MagicMock()
    mock_response.data = example_playlist_data

    with patch(
        "spotantic_mcp.tools.endpoints.playlists._create_playlist.create_playlist",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        name = "playlist name"
        public = True
        collaborative = True
        description = "playlist description"
        res = await create_playlist_tool(
            ctx=mock_context,
            name=name,
            public=public,
            collaborative=collaborative,
            description=description,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            name=name,
            public=public,
            collaborative=collaborative,
            description=description,
        )
        assert res == PlaylistView.model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_create_playlist_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "create_playlist_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
