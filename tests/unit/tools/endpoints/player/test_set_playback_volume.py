from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.player._set_playback_volume import set_playback_volume_tool


@pytest.mark.asyncio
async def test_set_playback_volume_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.player._set_playback_volume.set_playback_volume", new=AsyncMock()
    ) as mock_api_call:
        volume_percent = 1
        device_id = "devID"
        res = await set_playback_volume_tool(ctx=mock_context, volume_percent=volume_percent, device_id=device_id)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            volume_percent=volume_percent,
            device_id=device_id,
        )
        assert res == "Successfully set the volume for the user's current playback device."


@pytest.mark.asyncio
async def test_set_playback_volume_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "set_playback_volume_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
