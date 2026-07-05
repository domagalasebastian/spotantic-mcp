from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.utilities.scripts._remove_playlist_duplicated_items import remove_playlist_duplicated_items


@pytest.mark.asyncio
async def test_remove_playlist_duplicated_items_removes_duplicates(
    example_playlist_owner_data, example_track_data, example_episode_data
):
    duplicate_track = MagicMock()
    duplicate_track.item = example_track_data
    duplicate_track_again = MagicMock()
    duplicate_track_again.item = example_track_data
    unique_episode = MagicMock()
    unique_episode.item = example_episode_data

    client = MagicMock()

    with (
        patch(
            "spotantic_mcp.tools.utilities.scripts._remove_playlist_duplicated_items.get_all_playlist_items",
            new=AsyncMock(return_value=[duplicate_track, duplicate_track_again, unique_episode]),
        ) as mock_get_all_playlist_items,
        patch(
            "spotantic_mcp.tools.utilities.scripts._remove_playlist_duplicated_items.update_playlist_items",
            new=AsyncMock(),
        ) as mock_update_playlist_items,
        patch(
            "spotantic_mcp.tools.utilities.scripts._remove_playlist_duplicated_items.add_items_to_playlist",
            new=AsyncMock(),
        ) as mock_add_items_to_playlist,
    ):
        duplicated_count = await remove_playlist_duplicated_items(client, playlist_id="playlist-id")

    assert duplicated_count == 1
    mock_get_all_playlist_items.assert_awaited_once_with(client, playlist_id="playlist-id")
    mock_update_playlist_items.assert_awaited_once_with(
        client,
        playlist_id="playlist-id",
        uris=[example_track_data.track_uri, example_episode_data.episode_uri],
        range_start=0,
        insert_before=0,
    )
    mock_add_items_to_playlist.assert_not_awaited()
