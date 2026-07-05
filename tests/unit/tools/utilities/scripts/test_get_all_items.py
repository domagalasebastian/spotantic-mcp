from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel
from pydantic import HttpUrl
from spotantic.models.spotify import PagedResultModel

from spotantic_mcp.tools.utilities.scripts._get_all_items import get_all_items


class ExampleItem(BaseModel):
    id: int


@pytest.mark.asyncio
async def test_get_all_items_fetches_all_pages():
    first_page = MagicMock()
    second_page = MagicMock()
    third_page = MagicMock()
    first_page.data = PagedResultModel(
        items=[ExampleItem(id=1)],
        total=3,
        limit=1,
        offset=0,
        href=HttpUrl("https://api.spotify.com/v1/example"),
        next=None,
        previous=None,
    )
    second_page.data = PagedResultModel(
        items=[ExampleItem(id=2)],
        total=3,
        limit=1,
        offset=1,
        href=HttpUrl("https://api.spotify.com/v1/example"),
        next=None,
        previous=None,
    )
    third_page.data = PagedResultModel(
        items=[ExampleItem(id=3)],
        total=3,
        limit=1,
        offset=2,
        href=HttpUrl("https://api.spotify.com/v1/example"),
        next=None,
        previous=None,
    )

    responses = {0: first_page, 1: second_page, 2: third_page}

    async def fake_coroutine(*args: object, offset: int = 0, **kwargs: object):
        return responses[offset]

    items = await get_all_items(fake_coroutine)

    assert items == [ExampleItem(id=1), ExampleItem(id=2), ExampleItem(id=3)]
