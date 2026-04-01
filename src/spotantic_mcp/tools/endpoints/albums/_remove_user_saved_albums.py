from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.albums import remove_user_saved_albums

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def remove_user_saved_albums_tool(ctx: Context[ServerSession, AppContext], album_ids: list[str]) -> str:
    """Remove one or more albums from the current user's 'Your Music' library.

    Args:
        ctx: The tool context, which includes the server session and application context.
        album_ids: A list of Spotify IDs for the albums to be removed from the user's library.
         Each ID should be 22 alphanumeric characters (e.g. '4aawyAB9zYYRM4BVTNc75l'). Maximum of 20 IDs per request.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    await remove_user_saved_albums(spotantic_client, album_ids=album_ids)
    return f"Removed {len(album_ids)} album(s) from the user's library."
