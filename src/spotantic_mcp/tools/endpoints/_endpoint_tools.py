from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from .albums import album_endpoint_tools
from .artists import artist_endpoint_tools

endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify Endpoint Tools",
    tools=[
        album_endpoint_tools,
        artist_endpoint_tools,
    ],
)
