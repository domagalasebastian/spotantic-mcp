from typing import Literal

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.artists import get_artist_albums

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PagedResultView
from spotantic_mcp.tools.endpoints._views import SimplifiedAlbumView


@handle_spotantic_errors
async def get_artist_albums_tool(
    ctx: Context[ServerSession, AppContext],
    artist_id: str,
    limit: int = 10,
    offset: int = 0,
    market: str | None = None,
    include_groups: list[Literal["album", "single", "appears_on", "compilation"]] | None = None,
) -> PagedResultView[SimplifiedAlbumView]:
    """Get Spotify catalog information about an artist's albums.

    Use pagination (limit/offset) to fetch tracks in smaller chunks to minimize response size.
    For large albums, iterate through pages using offset += limit rather than fetching all at once.

    Args:
        ctx: The tool context, which includes the server session and application context.
        artist_id: The Spotify ID for the artist (22 alphanumeric characters).
        limit: The maximum number of items to return. Default: 10. Minimum: 1. Maximum: 50.
          Use smaller values (10-20) to get faster responses and avoid large JSON payloads.
        offset: The index of the first item to return. Default: 0 (the first item).
          Increment this to paginate through results: offset=10, offset=20, offset=30, etc.
        market: An ISO 3166-1 alpha-2 country code (2 letters, e.g. 'US', 'GB', 'PL').
        include_groups: A list of keywords that will be used to filter the response.
         If not supplied, all album types will be returned. Valid values are:
         'album', 'single', 'appears_on', 'compilation'.

    Returns:
        A paged result containing simplified album objects for the artist's albums.
        Check the 'total' field to know how many items exist and paginate accordingly.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_artist_albums(
            spotantic_client,
            artist_id=artist_id,
            limit=limit,
            offset=offset,
            market=market,
            include_groups=include_groups,  # type: ignore
        )
    ).data

    return PagedResultView[SimplifiedAlbumView].model_validate(api_data)
