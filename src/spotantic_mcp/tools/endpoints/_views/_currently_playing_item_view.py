from datetime import datetime
from datetime import timedelta

from pydantic import Field
from pydantic import field_validator
from spotantic.models.spotify.submodels import ContextModel
from spotantic.models.spotify.submodels import PlaybackActionsModel

from ._base_view import BaseView
from ._episode_view import EpisodeView
from ._track_view import TrackView


class CurrentlyPlayingItemView(BaseView):
    """Model representing the item currently being played on the user's Spotify account."""

    context: ContextModel | None = Field(None, description="A playback context.")
    """A playback context."""

    timestamp: datetime = Field(repr=False, description="Timestamp when playback state was last changed.")
    """Unix Millisecond Timestamp when playback state was last changed."""

    progress: timedelta = Field(
        alias="progress_ms", description="Progress into the currently playing track or episode."
    )
    """Progress into the currently playing track or episode."""

    is_playing: bool = Field(description="True if something is currently playing.")
    """`True` if something is currently playing."""

    item: TrackView | EpisodeView | None = Field(
        None, discriminator="item_type", description="The currently playing track or episode."
    )
    """The currently playing track or episode."""

    actions: PlaybackActionsModel = Field(
        repr=False,
        description=(
            "Allows to update the user interface based on which playback actions "
            "are available within the current context."
        ),
    )
    """Allows to update the user interface based on which playback actions are available within the current context."""

    @field_validator("progress", mode="before")
    def convert_progress_ms_to_timedelta(cls, value: int | timedelta) -> timedelta:
        """Converts track/episode progress given in milliseconds to `timedelta` object.

        Args:
            value: Track/Episode progress [milliseconds].

        Returns:
            Track/Episode progress as `timedelta` object.
        """
        if isinstance(value, timedelta):
            return value

        return timedelta(milliseconds=value)
