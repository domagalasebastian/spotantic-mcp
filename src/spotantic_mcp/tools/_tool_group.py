from __future__ import annotations

from collections.abc import Callable

from mcp.types import AnyFunction


class ToolGroup[T: AnyFunction]:
    def __init__(self, name: str, tools: list[T | ToolGroup[T]]) -> None:
        """A group of tools.

        Args:
            name: The name of the tool group.
            tools: A list of tools or tool groups that belong to this group.
        """
        self._name = name
        self._tools = tools

    @property
    def name(self) -> str:
        """The name of the tool group.

        Returns:
            The name of the tool group.
        """
        return self._name

    @property
    def tools(self) -> list[T | ToolGroup[T]]:
        """The tools in the tool group.

        Returns:
            A list of tools or tool groups that belong to this group.
        """
        return self._tools

    def add_tool(self, tool: T | ToolGroup[T]) -> None:
        """Add a tool to the tool group.

        Args:
            tool: The tool or tool group to add to the group.
        """
        self._tools.append(tool)

    def add_tool_decorator(self) -> Callable[[T], T]:
        """Decorator to add a tool to the tool group.

        Returns:
            A decorator function that adds the decorated tool or tool group to this group.
        """

        def decorator(tool: T) -> T:
            self.add_tool(tool)
            return tool

        return decorator
