from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.episodes._remove_user_saved_episodes import remove_user_saved_episodes_tool


@pytest.mark.asyncio
async def test_remove_user_saved_episodes_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.episodes._remove_user_saved_episodes.remove_user_saved_episodes", new=AsyncMock()
    ) as mock_api_call:
        episode_ids = ["123"]
        res = await remove_user_saved_episodes_tool(ctx=mock_context, episode_ids=episode_ids)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            episode_ids=episode_ids,
        )
        assert res == f"Removed {len(episode_ids)} episode(s) from the user's library."


@pytest.mark.asyncio
@pytest.mark.skip("Excluded from tools list since Library endpoint is available")
async def test_remove_user_saved_episodes_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "remove_user_saved_episodes_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
