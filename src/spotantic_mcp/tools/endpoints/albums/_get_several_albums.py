from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.albums import get_several_albums

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import SimplifiedAlbumView


@handle_spotantic_errors
async def get_several_albums_tool(
    ctx: Context[ServerSession, AppContext],
    album_ids: list[str],
    market: str | None = None,
) -> list[SimplifiedAlbumView]:
    """Get Spotify catalog information for multiple albums identified by their Spotify IDs.

    Args:
        ctx: The tool context, which includes the server session and application context.
        album_ids: A list of Spotify album IDs (each 22 alphanumeric characters).
          Each ID should be 22 alphanumeric characters (e.g. '4aawyAB9zYYRM4BVTNc75l'). Maximum of 20 IDs per request.
        market: An ISO 3166-1 alpha-2 country code (2 letters, e.g. 'US', 'GB', 'PL').

    Returns:
        A list of SimplifiedAlbumView objects containing information about the albums.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_several_albums(
            spotantic_client,
            album_ids=album_ids,
            market=market,
        )
    ).data

    return [SimplifiedAlbumView.model_validate(album_data) for album_data in api_data]
