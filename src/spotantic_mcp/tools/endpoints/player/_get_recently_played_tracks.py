from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import get_recently_played_tracks

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PagedResultWithCursorsView
from spotantic_mcp.tools.endpoints._views import PlayHistoryView


@handle_spotantic_errors
async def get_recently_played_tracks_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    limit: int = 10,
    after: int | None = None,
    before: int | None = None,
) -> PagedResultWithCursorsView[PlayHistoryView]:
    """Get tracks from the current user's recently played tracks.

    Use pagination (limit/cursors) to fetch tracks in smaller chunks to minimize response size.
    For large requests, iterate through pages using cursors (after/before) rather than fetching all at once.

    Args:
        ctx: The tool context, which includes the server session and application context.
        limit: The maximum number of items to return. Minimum is 1, maximum is 50. Use smaller values (10-20) to
          get faster responses and avoid large JSON payloads.
        after: A Unix timestamp in milliseconds. Returns all items after (but not including) this cursor position.
        before: A Unix timestamp in milliseconds. Returns all items before (but not including) this cursor position.

    Returns:
        A paged result containing recently played tracks and the cursors used to find the next set of items.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_recently_played_tracks(
            spotantic_client,
            limit=limit,
            after=after,
            before=before,
        )
    ).data

    return PagedResultWithCursorsView[PlayHistoryView].model_validate(api_data)
