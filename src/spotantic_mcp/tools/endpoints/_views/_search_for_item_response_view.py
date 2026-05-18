from ._base_view import BaseView
from ._paged_result_view import PagedResultView
from ._simplified_album_view import SimplifiedAlbumView
from ._simplified_artist_view import SimplifiedArtistView
from ._simplified_episode_view import SimplifiedEpisodeView
from ._simplified_playlist_view import SimplifiedPlaylistView
from ._simplified_show_view import SimplifiedShowView
from ._simplified_track_view import SimplifiedTrackView


class SearchForItemResponseView(BaseView):
    """Response model for Search For Item endpoint."""

    tracks: PagedResultView[SimplifiedTrackView] | None = None
    """List of tracks."""

    artists: PagedResultView[SimplifiedArtistView] | None = None
    """List of artists."""

    albums: PagedResultView[SimplifiedAlbumView] | None = None
    """List of albums."""

    playlists: PagedResultView[SimplifiedPlaylistView] | None = None
    """List of playlists."""

    shows: PagedResultView[SimplifiedShowView] | None = None
    """List of shows."""

    episodes: PagedResultView[SimplifiedEpisodeView] | None = None
    """List of episodes."""
