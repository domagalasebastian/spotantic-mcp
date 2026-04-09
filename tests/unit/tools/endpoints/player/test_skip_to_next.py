from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.player._skip_to_next import skip_to_next_tool


@pytest.mark.asyncio
async def test_skip_to_next_tool(mock_context):
    with patch("spotantic_mcp.tools.endpoints.player._skip_to_next.skip_to_next", new=AsyncMock()) as mock_api_call:
        res = await skip_to_next_tool(ctx=mock_context)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
        )
        assert res == "Successfully skipped to next track in the user's queue."


@pytest.mark.asyncio
async def test_skip_to_next_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "skip_to_next_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
