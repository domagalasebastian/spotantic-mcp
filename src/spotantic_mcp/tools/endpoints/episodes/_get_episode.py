from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.episodes import get_episode

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import EpisodeView


@handle_spotantic_errors
async def get_episode_tool(
    ctx: Context[ServerSession, AppContext], episode_id: str, market: str | None = None
) -> EpisodeView:
    """Get Spotify catalog information for a single episode.

    Args:
        ctx: The tool context, which includes the server session and application context.
        episode_id: The Spotify ID for the episode (22 alphanumeric characters, e.g. '4aawyAB9zYYRM4BVTNc75l').
        market: An ISO 3166-1 alpha-2 country code (2 letters, e.g. 'US', 'GB', 'PL').

    Returns:
        An EpisodeView containing information about the episode.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (await get_episode(spotantic_client, episode_id=episode_id, market=market)).data

    return EpisodeView.model_validate(api_data)
