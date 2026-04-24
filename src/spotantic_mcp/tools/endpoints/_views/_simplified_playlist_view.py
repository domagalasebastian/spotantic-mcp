from pydantic import Field

from ._playlist_base_view import PlaylistBaseView
from ._playlist_summary_view import PlaylistSummaryView


class SimplifiedPlaylistView(PlaylistBaseView):
    """Model representing simplified Spotify catalog information for a single playlist."""

    tracks: PlaylistSummaryView | None = Field(
        None,
        description=(
            "A collection containing a link ( href ) to the Web API endpoint where "
            "full details of the playlist's tracks can be retrieved."
        ),
    )
    """A collection containing a link ( href ) to the Web API endpoint where
    full details of the playlist's tracks can be retrieved."""
