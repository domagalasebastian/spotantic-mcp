import itertools
from collections import defaultdict
from operator import attrgetter

from spotantic.client import SpotanticClient
from spotantic.endpoints.playlists import add_items_to_playlist
from spotantic.endpoints.playlists import update_playlist_items
from spotantic.models.spotify import EpisodeModel
from spotantic.models.spotify import TrackModel

from ._get_all_playlist_items import get_all_playlist_items

UPDATE_PLAYLIST_ITEMS_LIMIT = 100
ADD_ITEMS_TO_PLAYLIST_LIMIT = 40


async def remove_playlist_duplicated_items(
    client: SpotanticClient,
    *,
    playlist_id: str,
) -> int:
    """Remove duplicated items from a playlist.

    Args:
        client: Spotantic client instance.
        playlist_id: The Spotify ID of the playlist.

    Returns:
        The number of duplicated items removed from the playlist.
    """
    all_items = await get_all_playlist_items(
        client,
        playlist_id=playlist_id,
    )

    uris_counter = defaultdict(int)
    for item in map(attrgetter("item"), all_items):
        match item:
            case TrackModel(track_uri=uri):
                item_uri = uri
            case EpisodeModel(episode_uri=uri):
                item_uri = uri
            case _:
                raise ValueError(f"Unsupported item type: {type(item)}")

        uris_counter[item_uri] += 1

    total_duplicated_items = 0
    unique_uris = []
    for uri, count in uris_counter.items():
        total_duplicated_items += count - 1
        unique_uris.append(uri)

    if not total_duplicated_items:
        return 0

    first_batch, remaining_items = unique_uris[:UPDATE_PLAYLIST_ITEMS_LIMIT], unique_uris[UPDATE_PLAYLIST_ITEMS_LIMIT:]

    # Remove all items from the playlist by reordering them to the start and then adding back the unique items
    await update_playlist_items(
        client,
        playlist_id=playlist_id,
        uris=first_batch,
        range_start=0,
        insert_before=0,
    )

    # Add the remaining unique items back to the playlist in batches of 40 keeping the order intact
    for batch in itertools.batched(remaining_items, ADD_ITEMS_TO_PLAYLIST_LIMIT):
        await add_items_to_playlist(
            client,
            playlist_id=playlist_id,
            uris=batch,
            position=None,
        )

    return total_duplicated_items
