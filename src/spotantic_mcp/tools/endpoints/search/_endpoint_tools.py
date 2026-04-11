from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from ._search_for_item import search_for_item_tool

search_endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify Search Endpoint Tools",
    tools=[
        search_for_item_tool,
    ],
)
