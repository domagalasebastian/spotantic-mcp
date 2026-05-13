from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.models.search.responses import SearchForItemResponse
from spotantic.models.spotify import PagedResultModel
from spotantic.types import SpotifyItemType

from spotantic_mcp.tools.endpoints._views import SearchForItemResponseView
from spotantic_mcp.tools.endpoints.search._search_for_item import search_for_item_tool


@pytest.mark.asyncio
async def test_search_for_item_tool(
    mock_context,
    example_track_data,
    example_artist_data,
    example_simplified_album_data,
    example_simplified_show_data,
    example_simplified_episode_data,
    example_simplified_playlist_data,
):
    tracks_result = PagedResultModel(
        href="https://api.spotify.com/v1/browse",  # type: ignore
        limit=1,
        next=None,
        total=1,
        offset=0,
        items=[example_track_data],
    )
    artists_result = PagedResultModel(
        href="https://api.spotify.com/v1/browse",  # type: ignore
        limit=1,
        next=None,
        total=1,
        offset=0,
        items=[example_artist_data],
    )
    albums_result = PagedResultModel(
        href="https://api.spotify.com/v1/browse",  # type: ignore
        limit=1,
        next=None,
        total=1,
        offset=0,
        items=[example_simplified_album_data],
    )
    shows_result = PagedResultModel(
        href="https://api.spotify.com/v1/browse",  # type: ignore
        limit=1,
        next=None,
        total=1,
        offset=0,
        items=[example_simplified_show_data],
    )
    episodes_result = PagedResultModel(
        href="https://api.spotify.com/v1/browse",  # type: ignore
        limit=1,
        next=None,
        total=1,
        offset=0,
        items=[example_simplified_episode_data],
    )
    playlists_result = PagedResultModel(
        href="https://api.spotify.com/v1/browse",  # type: ignore
        limit=1,
        next=None,
        total=1,
        offset=0,
        items=[example_simplified_playlist_data],
    )

    mock_response = MagicMock()
    mock_response.data = SearchForItemResponse(
        tracks=tracks_result,
        artists=artists_result,
        albums=albums_result,
        playlists=playlists_result,
        shows=shows_result,
        episodes=episodes_result,
    )

    with patch(
        "spotantic_mcp.tools.endpoints.search._search_for_item.search_for_item",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        item_type = ["album", "artist", "playlist", "track", "show", "episode"]
        item_type_enum = list(map(SpotifyItemType, item_type))
        res = await search_for_item_tool(
            ctx=mock_context,
            query="query",
            item_type=item_type,  # type: ignore
            market=None,
            limit=1,
            offset=0,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            query="query",
            item_type=item_type_enum,
            market=None,
            limit=1,
            offset=0,
        )
        assert res == SearchForItemResponseView.model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_search_for_item_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "search_for_item_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
