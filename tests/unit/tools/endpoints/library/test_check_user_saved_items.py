from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from spotantic_mcp.tools.endpoints.library._check_user_saved_items import check_user_saved_items_tool


@pytest.mark.asyncio
async def test_check_user_saved_items_tool(mock_context):
    mock_response = MagicMock()
    mock_response.data = {"uri1": True}

    with patch(
        "spotantic_mcp.tools.endpoints.library._check_user_saved_items.check_user_saved_items",
        new=AsyncMock(return_value=mock_response),
    ) as mock_api_call:
        res = await check_user_saved_items_tool(ctx=mock_context, uris=["uri1"])
        mock_api_call.assert_awaited_once_with(
            mock_context.request_context.lifespan_context.client,
            uris=["uri1"],
        )
        assert res == {"uri1": True}


@pytest.mark.asyncio
async def test_check_user_saved_items_tool_registered(test_server):
    tools = await test_server.list_tools()
    matching_tools = [tool for tool in tools if tool.name == "check_user_saved_items_tool"]
    assert len(matching_tools) == 1
    tool = matching_tools[0]
    assert tool.outputSchema is not None
