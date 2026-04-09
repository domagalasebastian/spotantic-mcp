from typing import Annotated

from pydantic import Field

from ._base_view import BaseView
from ._episode_view import EpisodeView
from ._track_view import TrackView


class GetUserQueueResponseView(BaseView):
    """Response model for Get User Queue endpoint."""

    currently_playing: TrackView | EpisodeView | None = Field(
        None, discriminator="item_type", description="The currently playing track or episode."
    )
    """The currently playing track or episode."""

    queue: list[Annotated[TrackView | EpisodeView, Field(discriminator="item_type")]] = Field(
        description="The tracks or episodes in the queue."
    )
    """The tracks or episodes in the queue."""
