from functools import partial

from spotantic.client import SpotanticClient
from spotantic.endpoints.playlists import get_playlist_items
from spotantic.models.spotify import PlaylistTrackModel
from spotantic.types import SpotifyItemType

from ._get_all_items import get_all_items

MAX_LIMIT = 50


async def get_all_playlist_items(
    client: SpotanticClient,
    *,
    playlist_id: str,
    fields: str | None = None,
    market: str | None = None,
) -> list[PlaylistTrackModel]:
    """Fetch all items from a playlist using pagination.

    Args:
        client: Spotantic client instance.
        playlist_id: The Spotify ID of the playlist.
        fields: Filters for the query: a comma-separated list of the fields to return.
        market: An ISO 3166-1 alpha-2 country code.

    Returns:
        A list containing all items retrieved from the playlist.
    """
    coro = partial(
        get_playlist_items,
        client,
        playlist_id=playlist_id,
        limit=MAX_LIMIT,
        fields=fields,
        additional_types=(SpotifyItemType.TRACK, SpotifyItemType.EPISODE),
        market=market,
    )

    return await get_all_items(coro)
