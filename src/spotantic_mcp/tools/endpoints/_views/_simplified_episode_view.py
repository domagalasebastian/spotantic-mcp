from datetime import date
from datetime import timedelta
from typing import Literal

from pydantic import Field
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

    release_date: date = Field(description="The date the episode was first released.")
    """The date the episode was first released."""

    resume_point: ResumePointModel | None = Field(
        None, repr=False, description="The user's most recent position in the episode."
    )
    """The user's most recent position in the episode"""

    item_type: Literal["episode"] = Field(alias="type", repr=False, description="The item type.")
    """The item type."""
