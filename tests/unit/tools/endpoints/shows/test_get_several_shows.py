from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints._views import SimplifiedShowView
from spotantic_mcp.tools.endpoints.shows._get_several_shows import get_several_shows_tool


@pytest.mark.asyncio
async def test_get_several_shows_tool(mock_context, example_simplified_show_data):
    mock_response = MagicMock()
    mock_response.data = [example_simplified_show_data]

    with patch(
        "spotantic_mcp.tools.endpoints.shows._get_several_shows.get_several_shows",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await get_several_shows_tool(ctx=mock_context, show_ids=[example_simplified_show_data.show_id])
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            show_ids=[example_simplified_show_data.show_id],
            market=None,
        )
        assert res == [SimplifiedShowView.model_validate(show) for show in mock_response.data]


@pytest.mark.asyncio
async def test_get_several_shows_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_several_shows_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
