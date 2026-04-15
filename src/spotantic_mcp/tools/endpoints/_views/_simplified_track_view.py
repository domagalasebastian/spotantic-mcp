from __future__ import annotations

from datetime import timedelta
from typing import Literal

from pydantic import Field
from spotantic.types import SpotifyItemID

from ._base_view import BaseView


class SimplifiedTrackView(BaseView):
    """Model representing simplified Spotify catalog information for a single track."""

    duration: timedelta = Field(alias="duration_ms", description="The track length in milliseconds.")
    """The track length in milliseconds."""

    track_id: SpotifyItemID = Field(alias="id", repr=False, description="The Spotify ID for the track.")
    """The Spotify ID for the track."""

    track_name: str = Field(alias="name", description="The name of the track.")
    """The name of the track."""

    item_type: Literal["track"] = Field(alias="type", repr=False, description="The item type.")
    """The item type."""
