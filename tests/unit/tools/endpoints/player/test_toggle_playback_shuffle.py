from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.player._toggle_playback_shuffle import toggle_playback_shuffle_tool


@pytest.mark.asyncio
async def test_toggle_playback_shuffle_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.player._toggle_playback_shuffle.toggle_playback_shuffle", new=AsyncMock()
    ) as mock_api_call:
        device_id = "devID"
        state = True
        res = await toggle_playback_shuffle_tool(ctx=mock_context, state=state, device_id=device_id)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            state=state,
            device_id=device_id,
        )
        assert res == "Successfully switched shuffle state for user's playback."


@pytest.mark.asyncio
async def test_toggle_playback_shuffle_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "toggle_playback_shuffle_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
