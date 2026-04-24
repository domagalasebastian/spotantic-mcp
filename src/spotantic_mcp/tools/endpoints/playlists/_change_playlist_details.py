from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.playlists import change_playlist_details

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def change_playlist_details_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    playlist_id: str,
    name: str | None = None,
    public: bool | None = None,
    collaborative: bool | None = None,
    description: str | None = None,
) -> str:
    """Change a playlist's name, description and/or public/private state.

    Args:
        ctx: The tool context, which includes the server session and application context.
        playlist_id: The Spotify ID of the playlist (22 alphanumeric characters, e.g. '4aawyAB9zYYRM4BVTNc75l').
        name: The new name for the playlist.
        public: Whether the playlist should be public.
        collaborative: Whether the playlist should be collaborative.
        description: The new description for the playlist.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    await change_playlist_details(
        spotantic_client,
        playlist_id=playlist_id,
        name=name,
        public=public,
        collaborative=collaborative,
        description=description,
    )
    return "Successfully changed the playlist data."
