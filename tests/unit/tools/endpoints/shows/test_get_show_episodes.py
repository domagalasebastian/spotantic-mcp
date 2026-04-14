from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.models.spotify import PagedResultModel

from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import SimplifiedEpisodeView
from spotantic_mcp.tools.endpoints.shows._get_show_episodes import get_show_episodes_tool


@pytest.mark.asyncio
async def test_get_show_episodes_tool(mock_context, example_simplified_episode_data):
    mock_response = MagicMock()
    mock_response.data = PagedResultModel(
        items=[example_simplified_episode_data],
        total=1,
        limit=1,
        offset=0,
        href="https://api.spotify.com/v1/shows/show123/episodes?offset=0&limit=1",  # type: ignore
    )

    with patch(
        "spotantic_mcp.tools.endpoints.shows._get_show_episodes.get_show_episodes",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await get_show_episodes_tool(
            ctx=mock_context,
            show_id="show123",
            limit=10,
            offset=0,
            market=None,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            show_id="show123",
            limit=10,
            offset=0,
            market=None,
        )
        assert res == PagedResultView[SimplifiedEpisodeView].model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_show_episodes_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_show_episodes_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
