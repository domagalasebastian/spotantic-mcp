from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.artists import get_several_artists

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import SimplifiedArtistView


@handle_spotantic_errors
async def get_several_artists_tool(
    ctx: Context[ServerSession, AppContext],
    artist_ids: list[str],
) -> list[SimplifiedArtistView]:
    """Get Spotify catalog information for several artists based on their Spotify IDs.

    Args:
        ctx: The tool context, which includes the server session and application context.
        artist_ids: A list of Spotify IDs for the artists (22 alphanumeric characters each).
          Maximum of 50 IDs per request.

    Returns:
        A list of SimplifiedArtistView objects containing information about the artists.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_several_artists(
            spotantic_client,
            artist_ids=artist_ids,
        )
    ).data

    return [SimplifiedArtistView.model_validate(artist_data) for artist_data in api_data]
