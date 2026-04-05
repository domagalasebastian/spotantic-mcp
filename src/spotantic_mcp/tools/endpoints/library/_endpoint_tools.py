from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from ._check_user_saved_items import check_user_saved_items_tool
from ._remove_items_from_library import remove_user_saved_items_tool
from ._save_items_to_library import save_items_to_library_tool

library_endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify Library Endpoint Tools",
    tools=[
        check_user_saved_items_tool,
        remove_user_saved_items_tool,
        save_items_to_library_tool,
    ],
)
