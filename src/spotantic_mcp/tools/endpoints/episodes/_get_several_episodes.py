from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.episodes import get_several_episodes

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import EpisodeView


@handle_spotantic_errors
async def get_several_episodes_tool(
    ctx: Context[ServerSession, AppContext],
    episode_ids: list[str],
    market: str | None = None,
) -> list[EpisodeView]:
    """Get Spotify catalog information for multiple episodes identified by their Spotify IDs.

    Args:
        ctx: The tool context, which includes the server session and application context.
        episode_ids: A list of Spotify episode IDs (each 22 alphanumeric characters).
          Each ID should be 22 alphanumeric characters (e.g. '4aawyAB9zYYRM4BVTNc75l'). Maximum of 50 IDs per request.
        market: An ISO 3166-1 alpha-2 country code (2 letters, e.g. 'US', 'GB', 'PL').

    Returns:
        A list of EpisodeView objects containing information about the episodes.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (
        await get_several_episodes(
            spotantic_client,
            episode_ids=episode_ids,
            market=market,
        )
    ).data

    return [EpisodeView.model_validate(episode_data) for episode_data in api_data]
