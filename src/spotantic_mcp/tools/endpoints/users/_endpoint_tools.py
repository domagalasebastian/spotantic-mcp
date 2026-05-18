from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from ._get_current_user_profile import get_current_user_profile_tool
from ._get_followed_artists import get_followed_artists_tool
from ._get_user_top_artists import get_user_top_artists_tool
from ._get_user_top_tracks import get_user_top_tracks_tool

user_endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify User Endpoint Tools",
    tools=[
        get_current_user_profile_tool,
        get_followed_artists_tool,
        get_user_top_artists_tool,
        get_user_top_tracks_tool,
    ],
)
