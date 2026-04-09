from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import get_user_queue

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import GetUserQueueResponseView


@handle_spotantic_errors
async def get_user_queue_tool(ctx: Context[ServerSession, AppContext]) -> GetUserQueueResponseView:
    """Get the list of objects that make up the user's queue.

    Args:
        ctx: The tool context, which includes the server session and application context.

    Returns:
        A GetUserQueueResponseView containing information about the currently playing tracks and
        tracks/episodes in the queue.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (await get_user_queue(spotantic_client)).data

    return GetUserQueueResponseView.model_validate(api_data)
