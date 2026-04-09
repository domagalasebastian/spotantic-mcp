from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.player._add_item_to_playback_queue import add_item_to_playback_queue_tool


@pytest.mark.asyncio
async def test_add_item_to_playback_queue_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.player._add_item_to_playback_queue.add_item_to_playback_queue", new=AsyncMock()
    ) as mock_api_call:
        uri = "uri1"
        res = await add_item_to_playback_queue_tool(ctx=mock_context, uri=uri, device_id=None)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            uri=uri,
            device_id=None,
        )
        assert res == f"Successfully added {uri} to the end of the user's playback queue."


@pytest.mark.asyncio
async def test_add_item_to_playback_queue_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "add_item_to_playback_queue_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
