from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import set_playback_volume

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def set_playback_volume_tool(
    ctx: Context[ServerSession, AppContext], *, volume_percent: int, device_id: str | None = None
) -> str:
    """Set the volume for the user's current playback device.

    Set the volume for the user’s current playback device. This API only works for users
    who have Spotify Premium. The order of execution is not guaranteed when you use this API with
    other Player API endpoints.

    Args:
        ctx: The tool context, which includes the server session and application context.
        volume_percent: The volume to set. Must be a value from 0 to 100 inclusive.
        device_id: The id of the device this command is targeting. If not supplied,
         the user's currently active device is the target.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    await set_playback_volume(spotantic_client, volume_percent=volume_percent, device_id=device_id)
    return "Successfully set the volume for the user's current playback device."
