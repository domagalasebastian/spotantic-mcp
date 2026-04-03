from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints._views import SimplifiedArtistView
from spotantic_mcp.tools.endpoints.artists._get_artist import get_artist_tool


@pytest.mark.asyncio
async def test_get_artist_tool(mock_context, example_simplified_artist_data):
    mock_response = MagicMock()
    mock_response.data = example_simplified_artist_data

    with patch(
        "spotantic_mcp.tools.endpoints.artists._get_artist.get_artist",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await get_artist_tool(
            ctx=mock_context,
            artist_id="artist123",
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            artist_id="artist123",
        )
        assert res == SimplifiedArtistView.model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_artist_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_artist_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
