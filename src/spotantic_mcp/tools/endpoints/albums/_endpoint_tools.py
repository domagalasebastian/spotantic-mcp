from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from ._check_user_saved_albums import check_user_saved_albums_tool
from ._get_album import get_album_tool
from ._get_album_artists import get_album_artists_tool
from ._get_album_tracks import get_album_tracks_tool
from ._get_new_releases import get_new_releases_tool
from ._get_several_albums import get_several_albums_tool
from ._get_user_saved_albums import get_user_saved_albums_tool
from ._remove_user_saved_albums import remove_user_saved_albums_tool
from ._save_albums_for_current_user import save_albums_for_current_user_tool

album_endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify Album Endpoint Tools",
    tools=[
        check_user_saved_albums_tool,
        get_album_tool,
        get_album_artists_tool,
        get_album_tracks_tool,
        get_new_releases_tool,
        get_several_albums_tool,
        get_user_saved_albums_tool,
        remove_user_saved_albums_tool,
        save_albums_for_current_user_tool,
    ],
)
