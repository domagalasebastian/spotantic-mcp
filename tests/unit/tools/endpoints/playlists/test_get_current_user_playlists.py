from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.models.spotify import PagedResultModel

from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import SimplifiedPlaylistView
from spotantic_mcp.tools.endpoints.playlists._get_current_user_playlists import get_current_user_playlist_tool


@pytest.mark.asyncio
async def test_get_current_user_playlist_tool(mock_context, example_simplified_playlist_data):
    mock_response = MagicMock()
    mock_response.data = PagedResultModel(
        items=[example_simplified_playlist_data],
        total=1,
        limit=1,
        offset=0,
        href="https://api.spotify.com/v1/browse/playlists?offset=0&limit=1",  # type: ignore
    )

    with patch(
        "spotantic_mcp.tools.endpoints.playlists._get_current_user_playlists.get_current_user_playlist",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        limit = 10
        offset = 0
        res = await get_current_user_playlist_tool(
            ctx=mock_context,
            limit=limit,
            offset=offset,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            limit=limit,
            offset=offset,
        )
        assert res == PagedResultView[SimplifiedPlaylistView].model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_current_user_playlist_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_current_user_playlist_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
