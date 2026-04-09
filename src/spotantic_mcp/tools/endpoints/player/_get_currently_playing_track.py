from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import get_currently_playing_track
from spotantic.types import SpotifyItemType

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import CurrentlyPlayingItemView


@handle_spotantic_errors
async def get_currently_playing_track_tool(
    ctx: Context[ServerSession, AppContext], *, market: str | None = None
) -> CurrentlyPlayingItemView:
    """Get the object currently being played on the user's Spotify account.

    Args:
        ctx: The tool context, which includes the server session and application context.
        market: An ISO 3166-1 alpha-2 country code.

    Returns:
        A CurrentlyPlayingItemView containing information about the item currently being
        played on the user's Spotify account.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    additional_types = (SpotifyItemType.TRACK, SpotifyItemType.EPISODE)
    api_data = (
        await get_currently_playing_track(
            spotantic_client,
            additional_types=additional_types,
            market=market,
        )
    ).data

    return CurrentlyPlayingItemView.model_validate(api_data)
