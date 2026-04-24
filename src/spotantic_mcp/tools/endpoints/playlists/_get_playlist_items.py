from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.playlists import get_playlist_items
from spotantic.types import SpotifyItemType

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import PlaylistTrackView


@handle_spotantic_errors
async def get_playlist_items_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    playlist_id: str,
    fields: str | None = None,
    limit: int = 10,
    offset: int = 0,
    market: str | None = None,
) -> PagedResultView[PlaylistTrackView]:
    """Get full details of the items of a playlist.

    Use pagination (limit/offset) to fetch playlists in smaller chunks to minimize response size.
    For large libraries, iterate through pages using offset += limit rather than fetching all at once.

    Args:
        ctx: The tool context, which includes the server session and application context.
        playlist_id: The Spotify ID of the playlist (22 alphanumeric characters, e.g. '4aawyAB9zYYRM4BVTNc75l').
        fields: Filters for the query: a comma-separated list of the fields to return. If omitted,
          all fields are returned. For example, to get just the total number of items and the request limit:
          'fields=total,limit'. A dot separator can be used to specify non-reoccurring fields, while parentheses can be
          used to specify reoccurring fields within objects. For example, to get just the added date and
          user ID of the adder: 'fields=items(added_at,added_by.id)'. Use multiple parentheses to drill down into
          nested objects, for example: 'fields=items(track(name,href,album(name,href)))'. Fields can be excluded by
          prefixing them with an exclamation mark, for example: 'fields=items.track.album(!external_urls,images)'.
        limit: The maximum number of items to return. Default: 10. Minimum: 1. Maximum: 50.
          Use smaller values (10-20) to get faster responses and avoid large JSON payloads.
        offset: The index of the first item to return. Default: 0 (the first item).
          Increment this to paginate through results: offset=10, offset=20, offset=30, etc.
        market: An ISO 3166-1 alpha-2 country code.

    Returns:
        A paged result containing playlist items for the playlists in the user's library.
        Check the 'total' field to know how many items exist and paginate accordingly.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    additional_types = (SpotifyItemType.TRACK, SpotifyItemType.EPISODE)
    api_data = (
        await get_playlist_items(
            spotantic_client,
            playlist_id=playlist_id,
            fields=fields,
            limit=limit,
            offset=offset,
            additional_types=additional_types,
            market=market,
        )
    ).data

    return PagedResultView[PlaylistTrackView].model_validate(api_data)
