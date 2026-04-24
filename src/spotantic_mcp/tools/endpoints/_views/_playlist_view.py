from pydantic import Field

from ._paged_result_view import PagedResultView
from ._playlist_base_view import PlaylistBaseView
from ._playlist_track_view import PlaylistTrackView


class PlaylistView(PlaylistBaseView):
    """Model representing a playlist owned by a Spotify user."""

    items: PagedResultView[PlaylistTrackView] = Field(description="The tracks of the playlist.")
    """The tracks of the playlist."""
