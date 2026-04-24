from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.playlists import get_playlist
from spotantic.types import SpotifyItemType

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PlaylistBaseView


@handle_spotantic_errors
async def get_playlist_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    playlist_id: str,
    market: str | None = None,
) -> PlaylistBaseView:
    """Get Spotify catalog information for a single playlist.

    Use `get_playlist_items_tool` to get the details about playlist items.

    Args:
        ctx: The tool context, which includes the server session and application context.
        playlist_id: The Spotify ID of the playlist (22 alphanumeric characters, e.g. '4aawyAB9zYYRM4BVTNc75l').
        market: An ISO 3166-1 alpha-2 country code.

    Returns:
        An PlaylistBaseView containing information about the playlist.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    additional_types = (SpotifyItemType.TRACK, SpotifyItemType.EPISODE)
    api_data = (
        await get_playlist(
            spotantic_client,
            playlist_id=playlist_id,
            fields=None,
            additional_types=additional_types,
            market=market,
        )
    ).data

    return PlaylistBaseView.model_validate(api_data)
