from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.playlists import remove_playlist_items
from spotantic.types import SpotifyEpisodeURI
from spotantic.types import SpotifyTrackURI

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def remove_playlist_items_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    playlist_id: str,
    uris: list[SpotifyEpisodeURI | SpotifyTrackURI],
    snapshot_id: str | None = None,
) -> str:
    """Remove one or more items from a user's playlist.

    Args:
        ctx: The tool context, which includes the server session and application context.
        playlist_id: The Spotify ID of the playlist (22 alphanumeric characters, e.g. '4aawyAB9zYYRM4BVTNc75l').
        uris: A list of Spotify URIs to be added. Each URI should be specified as 'spotify:<resource_type>:<id>'
          where resource_type specify an item: track or episode. Example: 'spotify:track:4aawyAB9zYYRM4BVTNc75l'.
          Maximum of 100 URIs per request. The list may contain different resource types in a single request.
        snapshot_id: The playlist's snapshot ID against which you want to make the changes.

    Returns:
        A string message representing the current snapshot ID of the playlist.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await remove_playlist_items(
            spotantic_client,
            playlist_id=playlist_id,
            uris=uris,
            snapshot_id=snapshot_id,
        )
    ).data
    return api_data.snapshot_id
