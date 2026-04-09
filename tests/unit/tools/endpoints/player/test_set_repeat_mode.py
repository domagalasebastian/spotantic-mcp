from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.player._set_repeat_mode import set_repeat_mode_tool


@pytest.mark.asyncio
async def test_set_repeat_mode_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.player._set_repeat_mode.set_repeat_mode", new=AsyncMock()
    ) as mock_api_call:
        state = "track"
        device_id = "devID"
        res = await set_repeat_mode_tool(ctx=mock_context, state=state, device_id=device_id)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            state=state,
            device_id=device_id,
        )
        assert res == "Successfully set the repeat mode for the user's current playback device."


@pytest.mark.asyncio
async def test_set_repeat_mode_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "set_repeat_mode_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
