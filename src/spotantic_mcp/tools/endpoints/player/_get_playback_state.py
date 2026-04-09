from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import get_playback_state
from spotantic.types import SpotifyItemType

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PlaybackStateView


@handle_spotantic_errors
async def get_playback_state_tool(
    ctx: Context[ServerSession, AppContext], *, market: str | None = None
) -> PlaybackStateView:
    """Get information about the user’s current playback state.

    Args:
        ctx: The tool context, which includes the server session and application context.
        market: An ISO 3166-1 alpha-2 country code.

    Returns:
        A PlaybackStateView containing information about the user’s current playback state.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    additional_types = (SpotifyItemType.TRACK, SpotifyItemType.EPISODE)
    api_data = (
        await get_playback_state(
            spotantic_client,
            additional_types=additional_types,
            market=market,
        )
    ).data

    return PlaybackStateView.model_validate(api_data)
