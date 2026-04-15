from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints._views import TrackView
from spotantic_mcp.tools.endpoints.tracks._get_track import get_track_tool


@pytest.mark.asyncio
async def test_get_track_tool(mock_context, example_track_data):
    mock_response = MagicMock()
    mock_response.data = example_track_data

    with patch(
        "spotantic_mcp.tools.endpoints.tracks._get_track.get_track", new=AsyncMock(return_value=mock_response)
    ) as mock_api_call:
        res = await get_track_tool(
            ctx=mock_context,
            track_id=example_track_data.track_id,
            market=None,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            track_id=example_track_data.track_id,
            market=None,
        )
        assert res == TrackView.model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_track_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_track_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
