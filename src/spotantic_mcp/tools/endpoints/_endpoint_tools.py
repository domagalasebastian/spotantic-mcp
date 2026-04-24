from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from .albums import album_endpoint_tools
from .artists import artist_endpoint_tools
from .episodes import episode_endpoint_tools
from .library import library_endpoint_tools
from .player import player_endpoint_tools
from .playlists import playlists_endpoint_tools
from .search import search_endpoint_tools
from .shows import show_endpoint_tools
from .tracks import track_endpoint_tools

endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify Endpoint Tools",
    tools=[
        album_endpoint_tools,
        artist_endpoint_tools,
        episode_endpoint_tools,
        library_endpoint_tools,
        player_endpoint_tools,
        playlists_endpoint_tools,
        search_endpoint_tools,
        show_endpoint_tools,
        track_endpoint_tools,
    ],
)
