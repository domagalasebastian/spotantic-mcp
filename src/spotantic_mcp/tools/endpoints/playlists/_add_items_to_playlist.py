from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.playlists import add_items_to_playlist

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def add_items_to_playlist_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    playlist_id: str,
    uris: list[str],
    position: int | None = None,
) -> str:
    """Add one or more items to a user's playlist.

    Only tracks or episodes can be added to a playlist.

    Args:
        ctx: The tool context, which includes the server session and application context.
        playlist_id: The Spotify ID of the playlist (22 alphanumeric characters, e.g. '4aawyAB9zYYRM4BVTNc75l').
        uris: A list of Spotify URIs to be added. Each URI should be specified as 'spotify:<resource_type>:<id>'
          where resource_type specify an item: track or episode. Example: 'spotify:track:4aawyAB9zYYRM4BVTNc75l'.
          Maximum of 40 URIs per request. The list may contain different resource types in a single request.
        position: The position to insert the items, or None to add to the end.

    Returns:
        A string message representing the current snapshot ID of the playlist.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await add_items_to_playlist(
            spotantic_client,
            playlist_id=playlist_id,
            uris=uris,
            position=position,
        )
    ).data
    return api_data.snapshot_id
