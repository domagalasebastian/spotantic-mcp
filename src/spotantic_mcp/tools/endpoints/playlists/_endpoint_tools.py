from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from ._add_items_to_playlist import add_items_to_playlist_tool
from ._change_playlist_details import change_playlist_details_tool
from ._create_playlist import create_playlist_tool
from ._get_current_user_playlists import get_current_user_playlist_tool
from ._get_playlist import get_playlist_tool
from ._get_playlist_items import get_playlist_items_tool
from ._remove_playlist_items import remove_playlist_items_tool
from ._update_playlist_items import update_playlist_items_tool

playlists_endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify Playlists Endpoint Tools",
    tools=[
        add_items_to_playlist_tool,
        change_playlist_details_tool,
        create_playlist_tool,
        get_current_user_playlist_tool,
        get_playlist_items_tool,
        get_playlist_tool,
        remove_playlist_items_tool,
        update_playlist_items_tool,
    ],
)
