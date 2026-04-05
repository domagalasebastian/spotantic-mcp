from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.library import check_user_saved_items

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def check_user_saved_items_tool(
    ctx: Context[ServerSession, AppContext],
    uris: list[str],
) -> dict[str, bool]:
    """Check if one or more items are already saved in the current user's library.

    Accepts Spotify URIs for tracks, albums, episodes, shows, audiobooks, artists, users, and playlists.
    For user and playlist types, it checks if the user follows the given item. Otherwise, checks whether
    the specified item is saved in the current user's library.

    Args:
        ctx: The tool context, which includes the server session and application context.
        uris: A list of Spotify URIs. Each URI should be specified as 'spotify:<resource_type>:<id>'
          where resource_type specify an item item e.g. track, album etc. Example:
          (e.g. 'spotify:track:4aawyAB9zYYRM4BVTNc75l'). Maximum of 40 URIs per request.
          The list may contain different resource types in a single request.

    Returns:
        A dictionary mapping each item ID to a boolean indicating whether it is saved/followed.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    return (await check_user_saved_items(spotantic_client, uris=uris)).data
