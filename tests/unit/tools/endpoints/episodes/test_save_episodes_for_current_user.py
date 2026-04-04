from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.episodes._save_episodes_for_current_user import save_episodes_for_current_user_tool


@pytest.mark.asyncio
async def test_save_episodes_for_current_user_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.episodes._save_episodes_for_current_user.save_episodes_for_current_user",
        new=AsyncMock(),
    ) as mock_api_call:
        episode_ids = ["123"]
        res = await save_episodes_for_current_user_tool(ctx=mock_context, episode_ids=episode_ids)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            episode_ids=episode_ids,
        )
        assert res == f"Saved {len(episode_ids)} episode(s) to the user's library."


@pytest.mark.asyncio
async def test_save_episodes_for_current_user_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "save_episodes_for_current_user_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
