from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints._views import SimplifiedAlbumView
from spotantic_mcp.tools.endpoints.albums._get_several_albums import get_several_albums_tool


@pytest.mark.asyncio
async def test_get_several_albums_tool(mock_context, example_album_data):
    mock_response = MagicMock()
    mock_response.data = [example_album_data]

    with patch(
        "spotantic_mcp.tools.endpoints.albums._get_several_albums.get_several_albums",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await get_several_albums_tool(ctx=mock_context, album_ids=[example_album_data.album_id])
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client, album_ids=[example_album_data.album_id], market=None
        )
        assert res == [SimplifiedAlbumView.model_validate(album) for album in mock_response.data]


@pytest.mark.asyncio
async def test_get_several_albums_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_several_albums_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
