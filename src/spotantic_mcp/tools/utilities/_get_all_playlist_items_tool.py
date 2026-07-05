from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PlaylistTrackView

from .scripts import get_all_playlist_items


@handle_spotantic_errors
async def get_all_playlist_items_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    playlist_id: str,
    fields: str | None = None,
    market: str | None = None,
) -> list[PlaylistTrackView]:
    """Get all items from a playlist using pagination.

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
        market: An ISO 3166-1 alpha-2 country code.

    Returns:
        A list containing all items retrieved from the playlist.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    items = await get_all_playlist_items(
        spotantic_client,
        playlist_id=playlist_id,
        fields=fields,
        market=market,
    )

    return [PlaylistTrackView.model_validate(item) for item in items]
