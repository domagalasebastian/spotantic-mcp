from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.shows import get_show_episodes

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import SimplifiedEpisodeView


@handle_spotantic_errors
async def get_show_episodes_tool(
    ctx: Context[ServerSession, AppContext],
    show_id: str,
    limit: int = 10,
    offset: int = 0,
    market: str | None = None,
) -> PagedResultView[SimplifiedEpisodeView]:
    """Get Spotify catalog information about an show’s episodes.

    Use pagination (limit/offset) to fetch episodes in smaller chunks to minimize response size.
    Iterate through pages using offset += limit rather than fetching all at once.

    Args:
        ctx: The tool context, which includes the server session and application context.
        show_id: The Spotify ID for the show (22 alphanumeric characters).
        limit: The maximum number of items to return. Default: 10. Minimum: 1. Maximum: 50.
          Use smaller values (10-20) to get faster responses and avoid large JSON payloads.
        offset: The index of the first item to return. Default: 0 (the first item).
          Increment this to paginate through results: offset=10, offset=20, offset=30, etc.
        market: An ISO 3166-1 alpha-2 country code (2 letters, e.g. 'US', 'GB', 'PL').

    Returns:
        A paged result containing simplified episode objects for the show's episodes.
        Check the 'total' field to know how many items exist and paginate accordingly.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_show_episodes(
            spotantic_client,
            show_id=show_id,
            limit=limit,
            offset=offset,
            market=market,
        )
    ).data

    return PagedResultView[SimplifiedEpisodeView].model_validate(api_data)
