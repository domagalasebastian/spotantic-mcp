from datetime import datetime

from pydantic import Field
from spotantic.types import AlbumTypes
from spotantic.types import SpotifyItemID

from ._base_view import BaseView


class SimplifiedAlbumView(BaseView):
    """Model representing simplified Spotify catalog information for a single album."""

    album_type: AlbumTypes = Field(description="The type of the album.")
    """The type of the album."""

    total_tracks: int = Field(description="The number of tracks in the album.")
    """The number of tracks in the album."""

    album_id: SpotifyItemID = Field(alias="id", repr=False, description="The Spotify ID for the album.")
    """The Spotify ID for the album."""

    album_name: str = Field(alias="name", description="The name of the album.")
    """The name of the album. In case of an album takedown, the value may be an empty string."""

    release_date: datetime = Field(description="The date the album was first released.")
    """The date the album was first released."""
