from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.models.spotify import PagedResultModel

from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import SavedShowView
from spotantic_mcp.tools.endpoints.shows._get_user_saved_shows import get_user_saved_shows_tool


@pytest.mark.asyncio
async def test_get_user_saved_shows_tool(mock_context, example_saved_show_data):
    mock_response = MagicMock()
    mock_response.data = PagedResultModel(
        items=[example_saved_show_data],
        total=1,
        limit=1,
        offset=0,
        href="https://api.spotify.com/v1/browse/saved?offset=0&limit=1",  # type: ignore
    )

    with patch(
        "spotantic_mcp.tools.endpoints.shows._get_user_saved_shows.get_user_saved_shows",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await get_user_saved_shows_tool(ctx=mock_context, limit=10, offset=0)
        mock_api_call.assert_awaited_once_with(mock_context.request_context.lifespan_context.client, limit=10, offset=0)
        assert res == PagedResultView[SavedShowView].model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_user_saved_shows_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_user_saved_shows_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
