from pydantic import Field

from ._base_view import BaseView


class PagedResultView[ItemT: BaseView](BaseView):
    """Model representing the information about paged result."""

    limit: int = Field(description="The maximum number of items in the response (as set in the query or by default).")
    """The maximum number of items in the response (as set in the query or by default)."""

    offset: int = Field(description="The offset of the items returned (as set in the query or by default).")
    """The offset of the items returned (as set in the query or by default)."""

    total: int = Field(description="The total number of items available to return.")
    """The total number of items available to return."""

    items: list[ItemT] = Field(description="An array of items collected from the current page.")
    """An array of items collected from the current page."""
