from pydantic import Field

from ._simplified_album_view import SimplifiedAlbumView
from ._simplified_track_view import SimplifiedTrackView


class TrackView(SimplifiedTrackView):
    """Model representing Spotify catalog information for a single track identified by its unique Spotify ID."""

    album: SimplifiedAlbumView = Field(description="The album on which the track appears.")
    """The album on which the track appears."""
