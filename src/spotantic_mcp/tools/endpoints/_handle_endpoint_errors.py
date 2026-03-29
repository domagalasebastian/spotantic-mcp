from collections.abc import Callable
from functools import wraps
from typing import Awaitable
from typing import ParamSpec
from typing import TypeVar

from mcp.server.fastmcp.exceptions import ToolError
from pydantic import ValidationError
from spotantic.types.exceptions import SpotanticException

P = ParamSpec("P")
R = TypeVar("R")


def handle_spotantic_errors(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    """Decorator to handle Spotantic API errors in endpoint tools.

    Catches exceptions raised by the Spotantic client and re-raises them as ToolError with
    appropriate messages for better error handling in the MCP client.

    Args:
        func: The async function to decorate. Should be an endpoint tool function.

    Returns:
        Wrapped function that handles Spotantic API errors and raises ToolError with user-friendly messages.
    """

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await func(*args, **kwargs)
        except SpotanticException as e:
            raise ToolError(
                f"Spotify API call failed! Exception class name: {e.__class__.__name__}, message: {str(e)}"
            ) from e
        except ValidationError as e:
            raise ToolError(f"Data validation failed! Exception message: {str(e)}") from e

    return wrapper
