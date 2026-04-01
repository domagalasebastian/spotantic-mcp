from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.albums import check_user_saved_albums

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def check_user_saved_albums_tool(
    ctx: Context[ServerSession, AppContext],
    album_ids: list[str],
) -> dict[str, bool]:
    """Check if one or more albums is already saved in the current Spotify user's 'Your Music' library.

    Args:
        ctx: The tool context, which includes the server session and application context.
        album_ids: A list of Spotify album IDs. Each ID should be 22 alphanumeric characters
          (e.g. '4aawyAB9zYYRM4BVTNc75l'). Maximum of 20 IDs per request.

    Returns:
        A dictionary mapping each album ID to a boolean indicating whether it is saved.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    return (await check_user_saved_albums(spotantic_client, album_ids=album_ids)).data
