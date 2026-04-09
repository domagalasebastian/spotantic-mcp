from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import transfer_playback

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def transfer_playback_tool(
    ctx: Context[ServerSession, AppContext], *, device_id: str, play: bool | None = None
) -> str:
    """Transfer playback to a new device.

    Transfer playback to a new device and optionally begin playback. This API only works for users
    who have Spotify Premium. The order of execution is not guaranteed when you use this API with
    other Player API endpoints.

    Args:
        ctx: The tool context, which includes the server session and application context.
        device_id: The id of the device on which playback should be started/transferred to.
        play: True to enable playback on the new device. If false or not provided,
         the user's current playback will continue on the previous device.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    await transfer_playback(spotantic_client, play=play, device_ids=[device_id])
    return "Successfully transferred playback to a new device."
