from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.shows import get_several_shows

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import SimplifiedShowView


@handle_spotantic_errors
async def get_several_shows_tool(
    ctx: Context[ServerSession, AppContext],
    show_ids: list[str],
    market: str | None = None,
) -> list[SimplifiedShowView]:
    """Get Spotify catalog information for multiple shows identified by their Spotify IDs.

    Args:
        ctx: The tool context, which includes the server session and application context.
        show_ids: A list of Spotify show IDs (each 22 alphanumeric characters).
          Each ID should be 22 alphanumeric characters (e.g. '4aawyAB9zYYRM4BVTNc75l'). Maximum of 50 IDs per request.
        market: An ISO 3166-1 alpha-2 country code (2 letters, e.g. 'US', 'GB', 'PL').

    Returns:
        A list of SimplifiedShowView objects containing information about the shows.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_several_shows(
            spotantic_client,
            show_ids=show_ids,
            market=market,
        )
    ).data

    return [SimplifiedShowView.model_validate(show_data) for show_data in api_data]
