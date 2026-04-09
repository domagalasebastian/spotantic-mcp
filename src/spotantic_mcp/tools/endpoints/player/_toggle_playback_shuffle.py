from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import toggle_playback_shuffle

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def toggle_playback_shuffle_tool(
    ctx: Context[ServerSession, AppContext], *, state: bool, device_id: str | None = None
) -> str:
    """Toggle shuffle state for user's playback.

    Toggle shuffle on or off for user’s playback. This API only works for users who have Spotify Premium.
    The order of execution is not guaranteed when you use this API with other Player API endpoints.

    Args:
        ctx: The tool context, which includes the server session and application context.
        state: True to turn shuffle on, False to turn it off.
        device_id: The id of the device this command is targeting. If not supplied,
         the user's currently active device is the target.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    await toggle_playback_shuffle(spotantic_client, state=state, device_id=device_id)
    return "Successfully switched shuffle state for user's playback."
