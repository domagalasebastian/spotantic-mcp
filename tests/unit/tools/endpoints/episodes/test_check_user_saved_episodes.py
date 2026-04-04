from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.episodes._check_user_saved_episodes import check_user_saved_episodes_tool


@pytest.mark.asyncio
async def test_check_user_saved_episodes_tool(mock_context):
    mock_response = MagicMock()
    mock_response.data = {"id1": True}

    with patch(
        "spotantic_mcp.tools.endpoints.episodes._check_user_saved_episodes.check_user_saved_episodes",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await check_user_saved_episodes_tool(ctx=mock_context, episode_ids=["123"])
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            episode_ids=["123"],
        )
        assert res == {"id1": True}


@pytest.mark.asyncio
async def test_check_user_saved_episodes_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "check_user_saved_episodes_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
