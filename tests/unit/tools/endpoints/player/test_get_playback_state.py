from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.types import SpotifyItemType

from spotantic_mcp.tools.endpoints._views import PlaybackStateView
from spotantic_mcp.tools.endpoints.player._get_playback_state import get_playback_state_tool


@pytest.mark.asyncio
async def test_get_playback_state_tool(mock_context, example_playback_state_data):
    mock_response = MagicMock()
    mock_response.data = example_playback_state_data

    with patch(
        "spotantic_mcp.tools.endpoints.player._get_playback_state.get_playback_state",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        additional_types = (SpotifyItemType.TRACK, SpotifyItemType.EPISODE)
        res = await get_playback_state_tool(ctx=mock_context, market=None)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            additional_types=additional_types,
            market=None,
        )
        assert res == PlaybackStateView.model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_playback_state_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_playback_state_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
