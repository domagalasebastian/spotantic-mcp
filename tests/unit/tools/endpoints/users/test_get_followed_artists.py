from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.models.spotify import ArtistModel
from spotantic.models.spotify import PagedResultWithCursorsModel
from spotantic.models.spotify.submodels import CursorsModel

from spotantic_mcp.tools.endpoints._views import PagedResultWithCursorsView
from spotantic_mcp.tools.endpoints._views import SimplifiedArtistView
from spotantic_mcp.tools.endpoints.users._get_followed_artists import get_followed_artists_tool


@pytest.mark.asyncio
async def test_get_followed_artists_tool(mock_context, example_artist_data):
    mock_response = MagicMock()
    mock_response.data = PagedResultWithCursorsModel[ArtistModel](
        href="https://api.spotify.com/v1/browse",  # type: ignore
        limit=1,
        next=None,
        total=None,
        cursors=CursorsModel(
            after="after",
            before="before",
        ),
        items=[example_artist_data],
    )

    with patch(
        "spotantic_mcp.tools.endpoints.users._get_followed_artists.get_followed_artists",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await get_followed_artists_tool(
            ctx=mock_context,
            limit=1,
            after=None,
        )
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            limit=1,
            after=None,
        )
        assert res == PagedResultWithCursorsView[SimplifiedArtistView].model_validate(mock_response.data)


@pytest.mark.asyncio
async def test_get_followed_artists_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "get_followed_artists_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
