from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.artists import get_artist_top_tracks

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import TrackView


@handle_spotantic_errors
async def get_artist_top_tracks_tool(
    ctx: Context[ServerSession, AppContext],
    artist_id: str,
    market: str | None = None,
) -> list[TrackView]:
    """Get Spotify catalog information about an artist's top tracks by country.

    Args:
        ctx: The tool context, which includes the server session and application context.
        artist_id: The Spotify ID for the artist (22 alphanumeric characters).
        market: An ISO 3166-1 alpha-2 country code (2 letters, e.g. 'US', 'GB', 'PL').

    Returns:
        A list of TrackView objects containing information about the artist's top tracks.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_artist_top_tracks(
            spotantic_client,
            artist_id=artist_id,
            market=market,
        )
    ).data

    return [TrackView.model_validate(track) for track in api_data]
