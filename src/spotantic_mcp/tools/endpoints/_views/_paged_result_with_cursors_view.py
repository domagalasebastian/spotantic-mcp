from pydantic import Field
from spotantic.models.spotify.submodels import CursorsModel

from ._base_view import BaseView


class PagedResultWithCursorsView[ItemT: BaseView](BaseView):
    """Model representing the information about paged result with cursors used to find the next set of items."""

    limit: int = Field(description="The maximum number of items in the response (as set in the query or by default).")
    """The maximum number of items in the response (as set in the query or by default)."""

    cursors: CursorsModel = Field(description="The cursors used to find the next set of items.")
    """The cursors used to find the next set of items."""

    items: list[ItemT] = Field(description="An array of items collected from the current page.")
    """An array of items collected from the current page."""
