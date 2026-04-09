from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.player._start_resume_playback import start_resume_playback_tool


@pytest.mark.asyncio
async def test_start_resume_playback_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.player._start_resume_playback.start_resume_playback", new=AsyncMock()
    ) as mock_api_call:
        device_id = "devID"
        context_uri = "uri1"
        offset = "uri2"
        position_ms = 10000
        res = await start_resume_playback_tool(
            ctx=mock_context,
            device_id=device_id,
            context_uri=context_uri,
            uris=None,
            offset=offset,
            position_ms=position_ms,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            device_id=device_id,
            context_uri=context_uri,
            uris=None,
            offset=offset,
            position_ms=position_ms,
        )
        assert res == "Successfully updated the user's playback."


@pytest.mark.asyncio
async def test_start_resume_playback_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "start_resume_playback_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
