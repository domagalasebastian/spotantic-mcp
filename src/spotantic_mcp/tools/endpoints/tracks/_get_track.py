from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.tracks import get_track

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import TrackView


@handle_spotantic_errors
async def get_track_tool(
    ctx: Context[ServerSession, AppContext], track_id: str, market: str | None = None
) -> TrackView:
    """Get Spotify catalog information for a single track.

    Args:
        ctx: The tool context, which includes the server session and application context.
        track_id: The Spotify ID for the track (22 alphanumeric characters, e.g. '4aawyAB9zYYRM4BVTNc75l').
        market: An ISO 3166-1 alpha-2 country code (2 letters, e.g. 'US', 'GB', 'PL').

    Returns:
        An TrackView containing information about the track.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (await get_track(spotantic_client, track_id=track_id, market=market)).data

    return TrackView.model_validate(api_data)
