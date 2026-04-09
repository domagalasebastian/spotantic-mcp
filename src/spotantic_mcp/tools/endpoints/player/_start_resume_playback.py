from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import start_resume_playback

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def start_resume_playback_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    device_id: str | None = None,
    context_uri: str | None = None,
    uris: list[str] | None = None,
    offset: int | str | None = None,
    position_ms: int | None = None,
) -> str:
    """Start or resume the user's playback.

    Start a new context or resume current playback on the user's active device. This API only works for users
    who have Spotify Premium. The order of execution is not guaranteed when you use this API with
    other Player API endpoints.

    Key notes:
        1. You can specify either context_uri or uris, but not both.
        2. The offset field is only available when context_uri corresponds to an album or a playlist.
        3. The offset field still applies when uris is specified.
        4. If neither context_uri nor uris is specified, the playback simply resumes the active context.

    Args:
        ctx: The tool context, which includes the server session and application context.
        device_id: The id of the device this command is targeting. If not supplied,
         the user's currently active device is the target.
        context_uri: Spotify URI of the context to play. Valid contexts are albums, artists, and playlists.
        uris: A list of Spotify track URIs to play. Each URI should be specified as 'spotify:track:<id>'.
          Example: 'spotify:track:4aawyAB9zYYRM4BVTNc75l'.
        offset: Indicates from where in the context playback should start.
         If an integer is provided, it is treated as a position index in the context.
         If a Spotify track URI is provided, playback will start from that track.
        position_ms: Indicates the position in milliseconds to start playback.

    Returns:
        A string message indicating the result of the operation.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    await start_resume_playback(
        spotantic_client,
        device_id=device_id,
        context_uri=context_uri,
        uris=uris,
        offset=offset,
        position_ms=position_ms,
    )
    return "Successfully updated the user's playback."
