from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from ._check_user_saved_episodes import check_user_saved_episodes_tool
from ._get_episode import get_episode_tool
from ._get_several_episodes import get_several_episodes_tool
from ._get_user_saved_episodes import get_user_saved_episodes_tool
from ._remove_user_saved_episodes import remove_user_saved_episodes_tool
from ._save_episodes_for_current_user import save_episodes_for_current_user_tool

episode_endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify Episode Endpoint Tools",
    tools=[
        check_user_saved_episodes_tool,
        get_episode_tool,
        get_several_episodes_tool,
        get_user_saved_episodes_tool,
        remove_user_saved_episodes_tool,
        save_episodes_for_current_user_tool,
    ],
)
