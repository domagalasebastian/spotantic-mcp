from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors

from .scripts import remove_playlist_duplicated_items


@handle_spotantic_errors
async def remove_playlist_duplicated_items_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    playlist_id: str,
) -> str:
    """Remove duplicated items from a playlist.

    Args:
        ctx: The tool context, which includes the server session and application context.
        playlist_id: The Spotify ID of the playlist.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client

    duplicated_count = await remove_playlist_duplicated_items(
        spotantic_client,
        playlist_id=playlist_id,
    )

    return f"Removed {duplicated_count} duplicated items from the playlist."
