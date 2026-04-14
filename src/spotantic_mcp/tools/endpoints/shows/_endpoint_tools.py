from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from ._get_several_shows import get_several_shows_tool
from ._get_show import get_show_tool
from ._get_show_episodes import get_show_episodes_tool
from ._get_user_saved_shows import get_user_saved_shows_tool

show_endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify Show Endpoint Tools",
    tools=[
        get_several_shows_tool,
        get_show_tool,
        get_show_episodes_tool,
        get_user_saved_shows_tool,
    ],
)
