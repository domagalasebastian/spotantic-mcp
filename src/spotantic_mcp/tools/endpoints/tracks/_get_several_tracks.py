from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.tracks import get_several_tracks

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import TrackView


@handle_spotantic_errors
async def get_several_tracks_tool(
    ctx: Context[ServerSession, AppContext],
    track_ids: list[str],
    market: str | None = None,
) -> list[TrackView]:
    """Get Spotify catalog information for multiple tracks identified by their Spotify IDs.

    Args:
        ctx: The tool context, which includes the server session and application context.
        track_ids: A list of Spotify track IDs (each 22 alphanumeric characters).
          Each ID should be 22 alphanumeric characters (e.g. '4aawyAB9zYYRM4BVTNc75l'). Maximum of 50 IDs per request.
        market: An ISO 3166-1 alpha-2 country code (2 letters, e.g. 'US', 'GB', 'PL').

    Returns:
        A list of TrackView objects containing information about the tracks.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_several_tracks(
            spotantic_client,
            track_ids=track_ids,
            market=market,
        )
    ).data

    return [TrackView.model_validate(track_data) for track_data in api_data]
