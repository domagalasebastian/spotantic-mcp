from datetime import datetime

from pydantic import Field

from ._base_view import BaseView
from ._simplified_show_view import SimplifiedShowView


class SavedShowView(BaseView):
    """Model representing a show saved in the current Spotify user's 'Your Music' library."""

    added_at: datetime = Field(
        description=(
            "The date and time the show was saved. Timestamps are returned in ISO 8601 format as "
            "Coordinated Universal Time (UTC) with a zero offset: YYYY-MM-DDTHH:MM:SSZ"
        )
    )
    """The date and time the show was saved. Timestamps are returned in ISO 8601 format as
    Coordinated Universal Time (UTC) with a zero offset: YYYY-MM-DDTHH:MM:SSZ"""

    show: SimplifiedShowView = Field(description="Information about the show.")
    """Information about the show."""
