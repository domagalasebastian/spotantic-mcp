from datetime import datetime

from pydantic import Field

from ._base_view import BaseView
from ._simplified_album_view import SimplifiedAlbumView


class SavedAlbumView(BaseView):
    """Model representing an album saved in the current Spotify user's 'Your Music' library."""

    added_at: datetime = Field(
        description=(
            "The date and time the album was saved. Timestamps are returned in ISO 8601 format as "
            "Coordinated Universal Time (UTC) with a zero offset: YYYY-MM-DDTHH:MM:SSZ"
        )
    )
    """The date and time the album was saved Timestamps are returned in ISO 8601 format as
    Coordinated Universal Time (UTC) with a zero offset: YYYY-MM-DDTHH:MM:SSZ"""

    album: SimplifiedAlbumView = Field(description="Information about the album.")
    """Information about the album."""
