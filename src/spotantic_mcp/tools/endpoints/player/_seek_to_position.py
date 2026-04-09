from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import seek_to_position

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def seek_to_position_tool(
    ctx: Context[ServerSession, AppContext], *, position_ms: int, device_id: str | None = None
) -> str:
    """Seek to position in currently playing track.

    Seeks to the given position in the user’s currently playing track. This API only works for users
    who have Spotify Premium. The order of execution is not guaranteed when you use this API with
    other Player API endpoints.

    Args:
        ctx: The tool context, which includes the server session and application context.
        position_ms: The position in milliseconds to seek to.
        device_id: The id of the device this command is targeting. If not supplied,
         the user's currently active device is the target.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    await seek_to_position(spotantic_client, position_ms=position_ms, device_id=device_id)
    return "Successfully changed position in currently playing track."
