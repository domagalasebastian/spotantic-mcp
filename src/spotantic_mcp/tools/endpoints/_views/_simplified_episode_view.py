from datetime import datetime
from datetime import timedelta
from typing import Literal

from pydantic import Field
from pydantic import field_validator
from spotantic.models.spotify.submodels import ResumePointModel
from spotantic.types import SpotifyItemID

from ._base_view import BaseView


class SimplifiedEpisodeView(BaseView):
    """Model representing simplified Spotify catalog information for a single episode."""

    description: str = Field(description="A description of the episode.")
    """A description of the episode."""

    duration: timedelta = Field(alias="duration_ms", description="The episode length in milliseconds.")
    """The episode length in milliseconds."""

    episode_id: SpotifyItemID = Field(alias="id", description="The Spotify ID for the episode.")
    """The Spotify ID for the episode."""

    episode_name: str = Field(alias="name", description="The name of the episode.")
    """The name of the episode."""

    release_date: datetime = Field(description="The date the episode was first released.")
    """The date the episode was first released."""

    resume_point: ResumePointModel | None = Field(
        None, repr=False, description="The user's most recent position in the episode."
    )
    """The user's most recent position in the episode"""

    item_type: Literal["episode"] = Field(alias="type", repr=False, exclude=True, description="The item type.")
    """The item type."""

    @field_validator("duration", mode="before")
    def convert_duration_ms_to_timedelta(cls, value: int | timedelta) -> timedelta:
        """Converts episode duration given in milliseconds to `timedelta` object.

        Args:
            value: Episode duration [milliseconds].

        Returns:
            Episode duration as `timedelta` object.
        """
        if isinstance(value, timedelta):
            return value

        return timedelta(milliseconds=value)
