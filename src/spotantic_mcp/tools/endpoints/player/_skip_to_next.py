from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import skip_to_next

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def skip_to_next_tool(ctx: Context[ServerSession, AppContext]) -> str:
    """Skip to next track in the user's queue.

    Skips to next track in the user’s queue. This API only works for users who have Spotify Premium.
    The order of execution is not guaranteed when you use this API with other Player API endpoints.

    Args:
        ctx: The tool context, which includes the server session and application context.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    await skip_to_next(spotantic_client)
    return "Successfully skipped to next track in the user's queue."
