from typing import Literal

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.users import get_user_top_items
from spotantic.models.users.requests import GetUserTopItemsTimeRange
from spotantic.models.users.requests import GetUserTopItemsType

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import SimplifiedArtistView


@handle_spotantic_errors
async def get_user_top_artists_tool(
    ctx: Context[ServerSession, AppContext],
    time_range: Literal["short_term", "medium_term", "long_term"] = "medium_term",
    limit: int = 20,
    offset: int = 0,
) -> PagedResultView[SimplifiedArtistView]:
    """Get the current user's top artists based on calculated affinity.

    Use pagination (limit/offset) to fetch artists in smaller chunks to minimize response size.
    For large libraries, iterate through pages using offset += limit rather than fetching all at once.

    Args:
        ctx: The tool context, which includes the server session and application context.
        time_range: Over what time frame the affinities are computed.
        limit: The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
          Use smaller values (10-20) to get faster responses and avoid large JSON payloads.
        offset: The index of the first item to return. Default: 0 (the first item).
          Increment this to paginate through results: offset=10, offset=20, offset=30, etc.

    Returns:
        A paged result containing simplified artist objects for the user's top artists.
        Check the 'total' field to know how many items exist and paginate accordingly.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_user_top_items(
            spotantic_client,
            item_type=GetUserTopItemsType.ARTISTS,
            time_range=GetUserTopItemsTimeRange(time_range),
            limit=limit,
            offset=offset,
        )
    ).data

    return PagedResultView[SimplifiedArtistView].model_validate(api_data)
