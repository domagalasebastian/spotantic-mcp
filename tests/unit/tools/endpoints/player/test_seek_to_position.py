from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.player._seek_to_position import seek_to_position_tool


@pytest.mark.asyncio
async def test_seek_to_position_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.player._seek_to_position.seek_to_position", new=AsyncMock()
    ) as mock_api_call:
        position_ms = 10000
        device_id = "devID"
        res = await seek_to_position_tool(ctx=mock_context, position_ms=position_ms, device_id=device_id)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            position_ms=position_ms,
            device_id=device_id,
        )
        assert res == "Successfully changed position in currently playing track."


@pytest.mark.asyncio
async def test_seek_to_position_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "seek_to_position_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
