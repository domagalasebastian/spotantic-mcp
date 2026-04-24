from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.playlists import update_playlist_items
from spotantic.types import SpotifyEpisodeURI
from spotantic.types import SpotifyTrackURI

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def update_playlist_items_tool(
    ctx: Context[ServerSession, AppContext],
    *,
    playlist_id: str,
    uris: list[SpotifyEpisodeURI | SpotifyTrackURI] | None = None,
    range_start: int,
    insert_before: int,
    range_length: int = 1,
    snapshot_id: str | None = None,
) -> str:
    """Reorder items in a playlist.

    Either reorder or replace items in a playlist depending on the request's parameters.
    To reorder items, include range_start, insert_before, range_length and snapshot_id in the request's body.
    To replace items, include uris as either a query parameter or in the request's body. Replacing items in
    a playlist will overwrite its existing items. This operation can be used for replacing or clearing items in
    a playlist. These operations can't be applied together in a single request. Examples:
    - To move the items at index 9-10 to the start of the playlist, range_start is set to 9, and range_length is
      set to 2.
    - To reorder the first item to the last position in a playlist with 10 items, set range_start to 0,
      and insert_before to 10.
    - To reorder the last item in a playlist with 10 items to the start of the playlist, set range_start to 9,
      and insert_before to 0.

    Args:
        ctx: The tool context, which includes the server session and application context.
        playlist_id: The Spotify ID of the playlist (22 alphanumeric characters, e.g. '4aawyAB9zYYRM4BVTNc75l').
        uris: A list of Spotify URIs to be added. Each URI should be specified as 'spotify:<resource_type>:<id>'
          where resource_type specify an item: track or episode. Example: 'spotify:track:4aawyAB9zYYRM4BVTNc75l'.
          Maximum of 100 URIs per request. The list may contain different resource types in a single request.
        range_start: The position of the first item to be reordered.
        insert_before: The position where the items should be inserted. To reorder the items to the end of the playlist,
          simply set insert_before to the position after the last item.
        range_length: The number of items to be reordered. Default is 1. The range of items to be reordered begins from
          the range_start position, and includes the range_length subsequent items.
        snapshot_id: The playlist's snapshot ID against which you want to make the changes.

    Returns:
        A string message representing the current snapshot ID of the playlist.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await update_playlist_items(
            spotantic_client,
            playlist_id=playlist_id,
            uris=uris,
            range_start=range_start,
            insert_before=insert_before,
            range_length=range_length,
            snapshot_id=snapshot_id,
        )
    ).data
    return api_data.snapshot_id
