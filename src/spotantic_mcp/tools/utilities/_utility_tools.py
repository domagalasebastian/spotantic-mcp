from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import UtilityTool

from ._get_all_playlist_items_tool import get_all_playlist_items_tool
from ._remove_playlist_duplicated_items_tool import remove_playlist_duplicated_items_tool

utility_tools = ToolGroup[UtilityTool](
    name="Spotify Utility Tools",
    tools=[
        get_all_playlist_items_tool,
        remove_playlist_duplicated_items_tool,
    ],
)
