from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.episodes import get_user_saved_episodes

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import SavedEpisodeView


@handle_spotantic_errors
async def get_user_saved_episodes_tool(
    ctx: Context[ServerSession, AppContext], limit: int = 10, offset: int = 0, market: str | None = None
) -> PagedResultView[SavedEpisodeView]:
    """Get a list of the episodes saved in the current Spotify user's 'Your Music' library.

    Use pagination (limit/offset) to fetch episodes in smaller chunks to minimize response size.
    For large libraries, iterate through pages using offset += limit rather than fetching all at once.

    Args:
        ctx: The tool context, which includes the server session and application context.
        limit: The maximum number of items to return. Default: 10. Minimum: 1. Maximum: 50.
          Use smaller values (10-20) to get faster responses and avoid large JSON payloads.
        offset: The index of the first item to return. Default: 0 (the first item).
          Increment this to paginate through results: offset=10, offset=20, offset=30, etc.
        market: An ISO 3166-1 alpha-2 country code.

    Returns:
        A paged result containing saved episode objects for the episodes in the user's library.
        Check the 'total' field to know how many items exist and paginate accordingly.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_user_saved_episodes(
            spotantic_client,
            limit=limit,
            offset=offset,
            market=market,
        )
    ).data

    return PagedResultView[SavedEpisodeView].model_validate(api_data)
