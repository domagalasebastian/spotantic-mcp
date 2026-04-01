"""Unit tests for the ToolGroup class."""

from spotantic_mcp.tools._tool_group import ToolGroup


# Mock tool functions for testing
def mock_tool_1() -> str:
    """Mock tool 1."""
    return "tool_1"


def mock_tool_2() -> str:
    """Mock tool 2."""
    return "tool_2"


def mock_tool_3() -> str:
    """Mock tool 3."""
    return "tool_3"


class TestToolGroup:
    """Test the ToolGroup class."""

    def test_tool_group_initialization(self) -> None:
        """Test ToolGroup initialization with name and tools."""
        group = ToolGroup(name="Test Group", tools=[mock_tool_1, mock_tool_2])

        assert group.name == "Test Group"
        assert group.tools == [mock_tool_1, mock_tool_2]
        assert len(group.tools) == 2

    def test_tool_group_with_nested_groups(self) -> None:
        """Test ToolGroup with nested ToolGroups."""
        sub_group = ToolGroup(name="Sub Group", tools=[mock_tool_3])
        main_group = ToolGroup(name="Main Group", tools=[mock_tool_1, sub_group])

        assert main_group.name == "Main Group"
        assert len(main_group.tools) == 2
        assert isinstance(main_group.tools[1], ToolGroup)
        assert main_group.tools[1].name == "Sub Group"

    def test_add_tool(self) -> None:
        """Test adding a tool to a ToolGroup."""
        group = ToolGroup(name="Test Group", tools=[mock_tool_1])
        assert len(group.tools) == 1

        group.add_tool(mock_tool_2)
        assert len(group.tools) == 2
        assert mock_tool_2 in group.tools

    def test_add_tool_group(self) -> None:
        """Test adding a ToolGroup to another ToolGroup."""
        sub_group = ToolGroup(name="Sub Group", tools=[mock_tool_2])
        main_group = ToolGroup(name="Main Group", tools=[mock_tool_1])

        main_group.add_tool(sub_group)
        assert len(main_group.tools) == 2
        assert sub_group in main_group.tools

    def test_add_tool_decorator(self) -> None:
        """Test using add_tool_decorator to add a tool."""
        group = ToolGroup(name="Test Group", tools=[])

        @group.add_tool_decorator()
        async def decorated_tool() -> str:
            """Decorated tool."""
            return "decorated"

        assert len(group.tools) == 1
        assert decorated_tool in group.tools

    def test_add_tool_decorator_with_multiple_tools(self) -> None:
        """Test using add_tool_decorator multiple times."""
        group = ToolGroup(name="Test Group", tools=[])

        @group.add_tool_decorator()
        async def tool_a() -> str:
            """Tool A."""
            return "a"

        @group.add_tool_decorator()
        async def tool_b() -> str:
            """Tool B."""
            return "b"

        assert len(group.tools) == 2
        assert tool_a in group.tools
        assert tool_b in group.tools

    def test_tool_group_empty_tools(self) -> None:
        """Test ToolGroup with empty tools list."""
        group = ToolGroup(name="Empty Group", tools=[])

        assert group.name == "Empty Group"
        assert group.tools == []
        assert len(group.tools) == 0
