from __future__ import annotations

from datetime import timedelta
from typing import Literal

from pydantic import Field
from pydantic import field_validator
from spotantic.types import SpotifyItemID
from spotantic.types import SpotifyTrackURI

from ._base_view import BaseView


class SimplifiedTrackView(BaseView):
    """Model representing simplified Spotify catalog information for a single track."""

    # TODO: Add get_track_artists_tool and remove artists field from this view.
    # artists: Sequence[SimplifiedArtistView] = Field(description="The artists who performed the track.")
    # """The artists who performed the track."""

    duration: timedelta = Field(alias="duration_ms", description="The track length in milliseconds.")
    """The track length in milliseconds."""

    track_id: SpotifyItemID = Field(alias="id", repr=False, description="The Spotify ID for the track.")
    """The Spotify ID for the track."""

    track_name: str = Field(alias="name", description="The name of the track.")
    """The name of the track."""

    item_type: Literal["track"] = Field(alias="type", repr=False, exclude=True, description="The item type.")
    """The item type."""

    track_uri: SpotifyTrackURI = Field(alias="uri", repr=False, description="The Spotify URI for the track.")
    """The Spotify URI for the track."""

    @field_validator("duration", mode="before")
    @classmethod
    def convert_duration_ms_to_timedelta(cls, value: int | timedelta) -> timedelta:
        """Converts track duration given in milliseconds to `timedelta` object.

        Args:
            value: Track duration [milliseconds].

        Returns:
            Track duration as `timedelta` object.
        """
        if isinstance(value, timedelta):
            return value

        return timedelta(milliseconds=value)
