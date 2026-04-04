from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints._views import EpisodeView
from spotantic_mcp.tools.endpoints.episodes._get_several_episodes import get_several_episodes_tool


@pytest.mark.asyncio
async def test_get_several_episodes_tool(mock_context, example_episode_data):
    mock_response = MagicMock()
    mock_response.data = [example_episode_data]

    with patch(
        "spotantic_mcp.tools.endpoints.episodes._get_several_episodes.get_several_episodes",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await get_several_episodes_tool(ctx=mock_context, episode_ids=[example_episode_data.episode_id])
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            episode_ids=[example_episode_data.episode_id],
            market=None,
        )
        assert res == [EpisodeView.model_validate(episode) for episode in mock_response.data]


@pytest.mark.asyncio
async def test_get_several_episodes_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_several_episodes_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
