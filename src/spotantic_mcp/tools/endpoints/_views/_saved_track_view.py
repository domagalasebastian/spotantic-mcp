from datetime import datetime

from pydantic import Field

from ._base_view import BaseView
from ._track_view import TrackView


class SavedTrackView(BaseView):
    """Model representing a track saved in the current Spotify user's 'Your Music' library."""

    added_at: datetime = Field(
        description=(
            "The date and time the track was saved. Timestamps are returned in ISO 8601 format as "
            "Coordinated Universal Time (UTC) with a zero offset: YYYY-MM-DDTHH:MM:SSZ"
        )
    )
    """The date and time the track was saved. Timestamps are returned in ISO 8601 format as
    Coordinated Universal Time (UTC) with a zero offset: YYYY-MM-DDTHH:MM:SSZ"""

    track: TrackView = Field(description="Information about the track.")
    """Information about the track."""
