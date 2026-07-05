import asyncio
import itertools
from typing import Any
from typing import Protocol

from pydantic import BaseModel
from spotantic.models import APICallModel
from spotantic.models.spotify import PagedResultModel


class PaginatedCall[T: BaseModel](Protocol):
    async def __call__(self, *args: Any, offset: int, **kwargs: Any) -> APICallModel[Any, Any, PagedResultModel[T]]: ...


async def get_all_items[T: BaseModel](coroutine_func: PaginatedCall[T]) -> list[T]:
    """Fetch all items from a paginated API endpoint.

    This function handles pagination by repeatedly calling the provided coroutine function
    until all items have been retrieved. It collects and returns all items in a single list.

    Args:
        coroutine_func: An awaitable coroutine function that fetches a page of items.

    Returns:
        A list containing all items retrieved from the paginated API endpoint.
    """
    data = (await coroutine_func(offset=0)).data
    all_items = list(data.items)

    if data.total <= len(data.items):
        return all_items

    tasks = []
    async with asyncio.TaskGroup() as tg:
        for offset in range(data.limit, data.total, data.limit):
            task = tg.create_task(coroutine_func(offset=offset))
            tasks.append(task)

    all_items.extend(itertools.chain.from_iterable(task.result().data.items for task in tasks))

    return all_items
