from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from ._get_several_tracks import get_several_tracks_tool
from ._get_track import get_track_tool
from ._get_user_saved_tracks import get_user_saved_tracks_tool

track_endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify Track Endpoint Tools",
    tools=[
        get_several_tracks_tool,
        get_track_tool,
        get_user_saved_tracks_tool,
    ],
)
