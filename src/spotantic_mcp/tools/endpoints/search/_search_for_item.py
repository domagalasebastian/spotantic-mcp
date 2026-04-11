from typing import Literal

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.search import search_for_item
from spotantic.types import SpotifyItemType

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import SearchForItemResponseView


@handle_spotantic_errors
async def search_for_item_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    query: str,
    item_type: list[Literal["album", "artist", "playlist", "track", "show", "episode"]],
    market: str | None = None,
    limit: int = 10,
    offset: int = 0,
) -> SearchForItemResponseView:
    """Search for specified items based on a provided query.

    Get Spotify catalog information about albums, artists, playlists, tracks, shows or
    episodes. Limit the number of item types to only require ones to minimize response size.

    Use pagination (limit/offset) to fetch episodes in smaller chunks to minimize response size.
    For large libraries, iterate through pages using offset += limit rather than fetching all at once.

    Args:
        ctx: The tool context, which includes the server session and application context.
        query: Your search query.
        item_type: A list of item types to search across. Search results include hits
          from all the specified item types.
        market: An ISO 3166-1 alpha-2 country code.
        limit: The maximum number of results to return in each item type. Maximum: 10.
          Use smaller values (5-10) to get faster responses and avoid large JSON payloads.
        offset: The index of the first result to return. Increment this to paginate through results:
          offset=10, offset=20, offset=30, etc.

    Returns:
        A SearchForItemResponseView containing information about the search results.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await search_for_item(
            spotantic_client,
            query=query,
            item_type=list(map(SpotifyItemType, item_type)),
            limit=limit,
            offset=offset,
            market=market,
        )
    ).data

    return SearchForItemResponseView.model_validate(api_data)
