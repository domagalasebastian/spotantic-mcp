from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.episodes import check_user_saved_episodes

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors


@handle_spotantic_errors
async def check_user_saved_episodes_tool(
    ctx: Context[ServerSession, AppContext],
    episode_ids: list[str],
) -> dict[str, bool]:
    """Check if one or more episodes is already saved in the current Spotify user's 'Your Episodes' library.

    Args:
        ctx: The tool context, which includes the server session and application context.
        album_ids: A list of Spotify episode IDs. Each ID should be 22 alphanumeric characters
          (e.g. '4aawyAB9zYYRM4BVTNc75l'). Maximum of 20 IDs per request.

    Returns:
        A dictionary mapping each episode ID to a boolean indicating whether it is saved.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    return (await check_user_saved_episodes(spotantic_client, episode_ids=episode_ids)).data
