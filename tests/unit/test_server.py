import pytest

from spotantic_mcp.server import create_server
from spotantic_mcp.tools import ToolGroup
from spotantic_mcp.tools import spotantic_mcp_tools


def test_create_server():
    server = create_server("Test Server")
    assert server is not None
    assert server.name == "Test Server"


@pytest.mark.asyncio
async def test_server_list_tools(test_server):
    tools = await test_server.list_tools()
    flatten_tools = []

    def flatten(tool_group):
        for tool in tool_group.tools:
            if isinstance(tool, ToolGroup):
                flatten(tool)
            else:
                flatten_tools.append(tool)

    flatten(spotantic_mcp_tools)
    tool_names = [tool.name for tool in tools]
    expected_tool_names = [tool.__name__ for tool in flatten_tools]

    assert set(tool_names) == set(expected_tool_names)
