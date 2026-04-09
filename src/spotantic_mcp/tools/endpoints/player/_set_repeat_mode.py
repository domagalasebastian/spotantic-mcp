from typing import Literal

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import set_repeat_mode
from spotantic.types import RepeatMode

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def set_repeat_mode_tool(
    ctx: Context[ServerSession, AppContext], *, state: Literal["track", "context", "off"], device_id: str | None = None
) -> str:
    """Set the repeat mode for the user's current playback device.

    Set the repeat mode for the user's playback. This API only works for users who have Spotify Premium.
    The order of execution is not guaranteed when you use this API with other Player API endpoints.

    Args:
        ctx: The tool context, which includes the server session and application context.
        state: The repeat mode to set. Possible values: track, context, off.
        device_id: The id of the device this command is targeting. If not supplied,
         the user's currently active device is the target.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client

    await set_repeat_mode(spotantic_client, state=RepeatMode(state), device_id=device_id)
    return "Successfully set the repeat mode for the user's current playback device."
