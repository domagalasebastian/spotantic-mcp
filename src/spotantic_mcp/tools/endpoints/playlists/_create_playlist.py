from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.playlists import create_playlist

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import PlaylistView


@handle_spotantic_errors
async def create_playlist_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    name: str,
    public: bool | None = None,
    collaborative: bool | None = None,
    description: str | None = None,
) -> PlaylistView:
    """Create a playlist for the current Spotify user.

    Each user is generally limited to a maximum of 11000 playlists.

    Args:
        ctx: The tool context, which includes the server session and application context.
        name: The name for the new playlist.
        public: Whether the playlist should be public.
        collaborative: Whether the playlist should be collaborative.
        description: The description for the new playlist.

    Returns:
        A PlaylistView containing information about the created playlist.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await create_playlist(
            spotantic_client,
            name=name,
            public=public,
            collaborative=collaborative,
            description=description,
        )
    ).data
    return PlaylistView.model_validate(api_data)
