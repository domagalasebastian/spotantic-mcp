from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from spotantic.types import SpotifyItemType

from spotantic_mcp.tools.utilities.scripts._get_all_playlist_items import get_all_playlist_items


@pytest.mark.asyncio
async def test_get_all_playlist_items_builds_pagination_coro(mock_context):
    expected_items = [MagicMock()]

    with patch(
        "spotantic_mcp.tools.utilities.scripts._get_all_playlist_items.get_all_items",
        new=AsyncMock(return_value=expected_items),
    ) as mock_get_all_items:
        items = await get_all_playlist_items(
            mock_context.request_context.lifespan_context.client,
            playlist_id="playlist-id",
            fields="field1,field2",
            market="US",
        )

    assert items == expected_items

    await_args = mock_get_all_items.await_args
    assert await_args is not None
    coro = await_args.args[0]
    assert coro.func.__name__ == "get_playlist_items"
    assert coro.args == (mock_context.request_context.lifespan_context.client,)
    assert coro.keywords["playlist_id"] == "playlist-id"
    assert coro.keywords["limit"] == 50
    assert coro.keywords["fields"] == "field1,field2"
    assert coro.keywords["additional_types"] == (SpotifyItemType.TRACK, SpotifyItemType.EPISODE)
    assert coro.keywords["market"] == "US"
