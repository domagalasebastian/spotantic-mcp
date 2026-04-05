from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.library._save_items_to_library import save_items_to_library_tool


@pytest.mark.asyncio
async def test_save_items_to_library_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.library._save_items_to_library.save_items_to_library",
        new=AsyncMock(),
    ) as mock_api_call:
        uris = ["uri1"]
        res = await save_items_to_library_tool(ctx=mock_context, uris=uris)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            uris=uris,
        )
        assert res == f"Saved {len(uris)} item(s) to the user's library."


@pytest.mark.asyncio
async def test_save_items_to_library_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "save_items_to_library_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
