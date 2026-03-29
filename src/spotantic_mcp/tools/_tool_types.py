from collections.abc import Callable
from typing import Awaitable
from typing import Concatenate
from typing import ParamSpec
from typing import TypeAlias
from typing import TypeVar

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

from spotantic_mcp._app_context import AppContext

P = ParamSpec("P")
R = TypeVar("R")

EndpointTool: TypeAlias = Callable[
    Concatenate[Context[ServerSession, AppContext], P],
    Awaitable[R],
]
