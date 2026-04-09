from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.player._pause_playback import pause_playback_tool


@pytest.mark.asyncio
async def test_pause_playback_tool(mock_context):
    with patch("spotantic_mcp.tools.endpoints.player._pause_playback.pause_playback", new=AsyncMock()) as mock_api_call:
        device_id = "devID"
        res = await pause_playback_tool(ctx=mock_context, device_id=device_id)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            device_id=device_id,
        )
        assert res == "Successfully paused playback on the user's account."


@pytest.mark.asyncio
async def test_pause_playback_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "pause_playback_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
