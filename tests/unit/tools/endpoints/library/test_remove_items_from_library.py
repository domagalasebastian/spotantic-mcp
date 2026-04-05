from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.library._remove_items_from_library import remove_user_saved_items_tool


@pytest.mark.asyncio
async def test_remove_user_saved_items_tool(mock_context):
    with patch(
        "spotantic_mcp.tools.endpoints.library._remove_items_from_library.remove_items_from_library", new=AsyncMock()
    ) as mock_api_call:
        uris = ["uri1"]
        res = await remove_user_saved_items_tool(ctx=mock_context, uris=uris)
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            uris=uris,
        )
        assert res == f"Removed {len(uris)} item(s) from the user's library."


@pytest.mark.asyncio
async def test_remove_user_saved_items_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "remove_user_saved_items_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
