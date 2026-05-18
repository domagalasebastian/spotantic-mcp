from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.users import get_current_user_profile

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import UserView


@handle_spotantic_errors
async def get_current_user_profile_tool(ctx: Context[ServerSession, AppContext]) -> UserView:
    """Get detailed profile information about the current user (including the current user's username).

    Args:
        ctx: The tool context, which includes the server session and application context.

    Returns:
        An UserView containing information about the current user.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_current_user_profile(
            spotantic_client,
        )
    ).data

    return UserView.model_validate(api_data)
