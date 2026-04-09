from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import add_item_to_playback_queue

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def add_item_to_playback_queue_tool(
    ctx: Context[ServerSession, AppContext], *, uri: str, device_id: str | None = None
) -> str:
    """Add an item to the end of the user's playback queue.

    Add an item to be played next in the user's current playback queue. This API only works for users
    who have Spotify Premium. The order of execution is not guaranteed when you use this API with
    other Player API endpoints.

    Args:
        ctx: The tool context, which includes the server session and application context.
        uri: The Spotify URI of the item to add to the queue. Must be a track or episode URI.
          URI should be specified as 'spotify:<resource_type>:<id>' where resource_type specify
          an item e.g. track, episode etc. Example: 'spotify:track:4aawyAB9zYYRM4BVTNc75l'.
        device_id: The id of the device this command is targeting. If not supplied,
         the user's currently active device is the target.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    await add_item_to_playback_queue(spotantic_client, uri=uri, device_id=device_id)
    return f"Successfully added {uri} to the end of the user's playback queue."
