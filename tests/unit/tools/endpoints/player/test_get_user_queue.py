from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.models.player.responses import GetUserQueueResponse

from spotantic_mcp.tools.endpoints._views import GetUserQueueResponseView
from spotantic_mcp.tools.endpoints.player._get_user_queue import get_user_queue_tool


@pytest.mark.asyncio
async def test_get_user_queue_tool(mock_context, example_episode_data, example_track_data):
    mock_response = MagicMock()
    mock_response.data = GetUserQueueResponse(
        currently_playing=example_track_data,
        queue=[example_episode_data, example_track_data],
    )

    with patch(
        "spotantic_mcp.tools.endpoints.player._get_user_queue.get_user_queue",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await get_user_queue_tool(ctx=mock_context)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
        )
        assert res == GetUserQueueResponseView.model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_user_queue_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_user_queue_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
