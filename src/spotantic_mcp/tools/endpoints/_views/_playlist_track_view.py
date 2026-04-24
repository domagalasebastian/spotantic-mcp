from datetime import datetime

from pydantic import Field

from ._base_view import BaseView
from ._episode_view import EpisodeView
from ._track_view import TrackView


class PlaylistTrackView(BaseView):
    """Model representing full details of the items of a playlist owned by a Spotify user."""

    added_at: datetime | None = Field(None, description="The date and time the track or episode was added.")
    """The date and time the track or episode was added."""

    is_local: bool = Field(repr=False, description="Whether this track or episode is a local file or not.")
    """Whether this track or episode is a local file or not."""

    item: TrackView | EpisodeView = Field(
        discriminator="item_type", description="Information about the track or episode."
    )
    """Information about the track or episode."""
