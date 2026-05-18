from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.models.spotify import PagedResultModel
from spotantic.models.spotify import TrackModel
from spotantic.models.users.requests import GetUserTopItemsTimeRange
from spotantic.models.users.requests import GetUserTopItemsType

from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import TrackView
from spotantic_mcp.tools.endpoints.users._get_user_top_tracks import get_user_top_tracks_tool


@pytest.mark.asyncio
async def test_get_user_top_tracks_tool(mock_context, example_track_data):
    mock_response = MagicMock()
    mock_response.data = PagedResultModel[TrackModel](
        href="https://api.spotify.com/v1/browse",  # type: ignore
        limit=1,
        next=None,
        total=1,
        offset=0,
        items=[example_track_data],
    )

    with patch(
        "spotantic_mcp.tools.endpoints.users._get_user_top_tracks.get_user_top_items",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await get_user_top_tracks_tool(
            ctx=mock_context,
            time_range="medium_term",
            limit=1,
            offset=0,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            item_type=GetUserTopItemsType.TRACKS,
            time_range=GetUserTopItemsTimeRange.MEDIUM_TERM,
            limit=1,
            offset=0,
        )
        assert res == PagedResultView[TrackView].model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_user_top_tracks_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_user_top_tracks_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
