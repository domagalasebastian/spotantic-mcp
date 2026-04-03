from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from ._get_artist import get_artist_tool
from ._get_artist_albums import get_artist_albums_tool
from ._get_artist_top_tracks import get_artist_top_tracks_tool
from ._get_several_artists import get_several_artists_tool

artist_endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify Artist Endpoint Tools",
    tools=[
        get_artist_tool,
        get_artist_albums_tool,
        get_artist_top_tracks_tool,
        get_several_artists_tool,
    ],
)
