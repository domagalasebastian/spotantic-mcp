from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.users import get_followed_artists

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PagedResultWithCursorsView
from spotantic_mcp.tools.endpoints._views import SimplifiedArtistView


@handle_spotantic_errors
async def get_followed_artists_tool(
    ctx: Context[ServerSession, AppContext], limit: int = 20, after: str | None = None
) -> PagedResultWithCursorsView[SimplifiedArtistView]:
    """Get the current user's followed artists.

    Use pagination (limit/cursors) to fetch artists in smaller chunks to minimize response size.

    Args:
        ctx: The tool context, which includes the server session and application context.
        limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50. Use smaller values (10-20)
          to get faster responses and avoid large JSON payloads.
        after: The last artist ID retrieved from the previous request.
          Used to get the next set of results.

    Returns:
        A paged result containing simplified artist objects for the artists followed by the user and
        the cursors used to find the next set of items.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_followed_artists(
            spotantic_client,
            limit=limit,
            after=after,
        )
    ).data

    return PagedResultWithCursorsView[SimplifiedArtistView].model_validate(api_data)
