from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.shows import get_show

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import SimplifiedShowView


@handle_spotantic_errors
async def get_show_tool(
    ctx: Context[ServerSession, AppContext], show_id: str, market: str | None = None
) -> SimplifiedShowView:
    """Get Spotify catalog information for a single show.

    Args:
        ctx: The tool context, which includes the server session and application context.
        show_id: The Spotify ID for the show (22 alphanumeric characters, e.g. '4aawyAB9zYYRM4BVTNc75l').
        market: An ISO 3166-1 alpha-2 country code (2 letters, e.g. 'US', 'GB', 'PL').

    Returns:
        An SimplifiedShowView containing information about the show.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (await get_show(spotantic_client, show_id=show_id, market=market)).data

    return SimplifiedShowView.model_validate(api_data)
