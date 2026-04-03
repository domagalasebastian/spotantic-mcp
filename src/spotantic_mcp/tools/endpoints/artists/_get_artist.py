from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.artists import get_artist

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import SimplifiedArtistView


@handle_spotantic_errors
async def get_artist_tool(
    ctx: Context[ServerSession, AppContext],
    artist_id: str,
) -> SimplifiedArtistView:
    """Get Spotify catalog information for a single artist identified by their unique Spotify ID.

    Args:
        ctx: The tool context, which includes the server session and application context.
        artist_id: The Spotify ID for the artist (22 alphanumeric characters).

    Returns:
        A SimplifiedArtistView containing information about the artist.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_artist(
            spotantic_client,
            artist_id=artist_id,
        )
    ).data

    return SimplifiedArtistView.model_validate(api_data)
