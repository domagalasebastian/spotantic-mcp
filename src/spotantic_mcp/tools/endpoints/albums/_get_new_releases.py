from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.albums import get_new_releases

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import SimplifiedAlbumView


@handle_spotantic_errors
async def get_new_releases_tool(
    ctx: Context[ServerSession, AppContext],
    limit: int = 10,
    offset: int = 0,
) -> PagedResultView[SimplifiedAlbumView]:
    """Get a list of new album releases featured in Spotify (shown, for example, on a Spotify player's "Browse" tab).

    Use pagination (limit/offset) to fetch releases in smaller chunks to minimize response size.
    For browsing, iterate through pages using offset += limit rather than fetching all at once.

    Args:
        ctx: The tool context, which includes the server session and application context.
        limit: The maximum number of items to return. Default: 10. Minimum: 1. Maximum: 50.
          Use smaller values (10-20) to get faster responses and avoid large JSON payloads.
        offset: The index of the first item to return. Default: 0 (the first item).
          Increment this to paginate through results: offset=10, offset=20, offset=30, etc.

    Returns:
        A paged result containing simplified album objects for the new releases.
        Check the 'total' field to know how many items exist and paginate accordingly.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_new_releases(
            spotantic_client,
            limit=limit,
            offset=offset,
        )
    ).data

    return PagedResultView[SimplifiedAlbumView].model_validate(api_data)
