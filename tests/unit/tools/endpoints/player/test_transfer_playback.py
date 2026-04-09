from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.player._transfer_playback import transfer_playback_tool


@pytest.mark.asyncio
async def test_transfer_playback_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.player._transfer_playback.transfer_playback", new=AsyncMock()
    ) as mock_api_call:
        device_id = "devID"
        play = True
        res = await transfer_playback_tool(ctx=mock_context, play=play, device_id=device_id)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            play=play,
            device_ids=[device_id],
        )
        assert res == "Successfully transferred playback to a new device."


@pytest.mark.asyncio
async def test_transfer_playback_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "transfer_playback_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
