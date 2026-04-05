from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.library import remove_items_from_library

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def remove_user_saved_items_tool(ctx: Context[ServerSession, AppContext], uris: list[str]) -> str:
    """Remove one or more items from the current user's library.

    Accepts Spotify URIs for tracks, albums, episodes, shows, audiobooks, artists, users, and playlists.
    For user and playlist types, it unfollows the given item. Otherwise, removes the specified item from
    the current user's library.

    Args:
        ctx: The tool context, which includes the server session and application context.
        uris: A list of Spotify URIs. Each URI should be specified as 'spotify:<resource_type>:<id>'
          where resource_type specify an item item e.g. track, album etc. Example:
          (e.g. 'spotify:track:4aawyAB9zYYRM4BVTNc75l'). Maximum of 40 URIs per request.
          The list may contain different resource types in a single request.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    await remove_items_from_library(spotantic_client, uris=uris)
    return f"Removed {len(uris)} item(s) from the user's library."
