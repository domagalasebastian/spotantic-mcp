from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.albums import get_album

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import SimplifiedArtistView


@handle_spotantic_errors
async def get_album_artists_tool(
    ctx: Context[ServerSession, AppContext], album_id: str, market: str | None = None
) -> list[SimplifiedArtistView]:
    """Get the artists of a single album.

    Args:
        ctx: The tool context, which includes the server session and application context.
        album_id: The Spotify ID for the album (22 alphanumeric characters, e.g. '4aawyAB9zYYRM4BVTNc75l').
        market: An ISO 3166-1 alpha-2 country code (2 letters, e.g. 'US', 'GB', 'PL').

    Returns:
        A list of SimplifiedArtistView objects containing information about the artists.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (await get_album(spotantic_client, album_id=album_id, market=market)).data

    return [SimplifiedArtistView.model_validate(artist_data) for artist_data in api_data.artists]
