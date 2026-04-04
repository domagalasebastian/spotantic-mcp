from datetime import datetime

from pydantic import Field

from ._base_view import BaseView
from ._episode_view import EpisodeView


class SavedEpisodeView(BaseView):
    """Model representing an episode saved in the current Spotify user's 'Your Music' library."""

    added_at: datetime = Field(
        description=(
            "The date and time the episode was saved. Timestamps are returned in ISO 8601 format as "
            "Coordinated Universal Time (UTC) with a zero offset: YYYY-MM-DDTHH:MM:SSZ"
        )
    )
    """The date and time the episode was saved Timestamps are returned in ISO 8601 format as
    Coordinated Universal Time (UTC) with a zero offset: YYYY-MM-DDTHH:MM:SSZ"""

    episode: EpisodeView = Field(description="Information about the episode.")
    """Information about the episode."""
