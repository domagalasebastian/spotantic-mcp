from datetime import datetime
from unittest.mock import MagicMock

import pytest
from spotantic.models.spotify import AlbumModel
from spotantic.models.spotify import ArtistModel
from spotantic.models.spotify import CurrentlyPlayingItemModel
from spotantic.models.spotify import DeviceModel
from spotantic.models.spotify import EpisodeModel
from spotantic.models.spotify import PagedResultModel
from spotantic.models.spotify import PlaybackStateModel
from spotantic.models.spotify import PlayHistoryModel
from spotantic.models.spotify import PlaylistModel
from spotantic.models.spotify import PlaylistSummaryModel
from spotantic.models.spotify import PlaylistTrackModel
from spotantic.models.spotify import SavedAlbumModel
from spotantic.models.spotify import SavedEpisodeModel
from spotantic.models.spotify import SavedShowModel
from spotantic.models.spotify import SavedTrackModel
from spotantic.models.spotify import SimplifiedAlbumModel
from spotantic.models.spotify import SimplifiedArtistModel
from spotantic.models.spotify import SimplifiedEpisodeModel
from spotantic.models.spotify import SimplifiedPlaylistModel
from spotantic.models.spotify import SimplifiedShowModel
from spotantic.models.spotify import SimplifiedTrackModel
from spotantic.models.spotify import TrackModel
from spotantic.models.spotify.submodels import ExternalUrlsModel
from spotantic.models.spotify.submodels import PlaybackActionsModel
from spotantic.models.spotify.submodels import PlaylistOwnerModel
from spotantic.types import AlbumTypes

from spotantic_mcp.server import create_server


@pytest.fixture
def test_server():
    mcp = create_server("Test MCP Server")
    return mcp


@pytest.fixture
def mock_context():
    mock_client = MagicMock()
    context = MagicMock()
    context.request_context.lifespan_context.client = mock_client

    return context


@pytest.fixture
def example_simplified_artist_data():
    return SimplifiedArtistModel(
        external_urls=ExternalUrlsModel(),
        href="https://api.spotify.com/v1/artists/250b0Wlc5Vk0CoUsaCY84M",  # type: ignore
        id="250b0Wlc5Vk0CoUsaCY84M",
        name="Example Artist",
        type="artist",
        uri="spotify:artist:250b0Wlc5Vk0CoUsaCY84M",
    )


@pytest.fixture
def example_artist_data(example_simplified_artist_data):
    return ArtistModel(
        **example_simplified_artist_data.model_dump(),
        genres=[],
        images=[],
    )


@pytest.fixture
def example_simplified_track_data(example_simplified_artist_data):
    return SimplifiedTrackModel(
        artists=[example_simplified_artist_data],
        available_markets=None,
        disc_number=1,
        duration_ms=180000,  # type: ignore
        explicit=False,
        external_urls=ExternalUrlsModel(),
        href="https://api.spotify.com/v1/tracks/7L0dopNg5r1I6OHcVpA47E",  # type: ignore
        id="7L0dopNg5r1I6OHcVpA47E",
        is_playable=True,
        linked_from=None,
        restrictions=None,
        name="Example Track",
        preview_url=None,
        track_number=1,
        type="track",
        uri="spotify:track:7L0dopNg5r1I6OHcVpA47E",
        is_local=False,
    )


@pytest.fixture
def example_simplified_album_data(example_simplified_artist_data):
    return SimplifiedAlbumModel(
        album_type=AlbumTypes.ALBUM,
        total_tracks=1,
        available_markets=None,
        external_urls=ExternalUrlsModel(),
        href="https://api.spotify.com/v1/albums/4LOrSSPct7B6yCzW1IltRd",  # type: ignore
        id="4LOrSSPct7B6yCzW1IltRd",
        images=[],
        name="Example Album",
        release_date="2024-01-01",  # type: ignore
        release_date_precision="day",
        restrictions=None,
        type="album",
        uri="spotify:album:4LOrSSPct7B6yCzW1IltRd",
        artists=[example_simplified_artist_data],
        album_group=None,
    )


@pytest.fixture
def example_album_data(example_simplified_album_data, example_simplified_track_data):
    return AlbumModel(
        **example_simplified_album_data.model_dump(),
        tracks=PagedResultModel(
            items=[example_simplified_track_data],
            total=1,
            limit=1,
            offset=0,
            href="https://api.spotify.com/v1/albums/4LOrSSPct7B6yCzW1IltRd/tracks",  # type: ignore
            next=None,
            previous=None,
        ),
        copyrights=[],
        external_ids=None,
        genres=[],
        label=None,
        popularity=None,
    )


@pytest.fixture
def example_saved_album_data(example_album_data):
    return SavedAlbumModel(
        added_at="2024-01-01T00:00:00Z",  # type: ignore
        album=example_album_data,
    )


@pytest.fixture
def example_track_data(example_simplified_track_data, example_simplified_album_data):
    return TrackModel(
        **example_simplified_track_data.model_dump(exclude={"duration"}),
        duration_ms=180000,  # type: ignore
        album=example_simplified_album_data,
    )


@pytest.fixture
def example_simplified_show_data():
    return SimplifiedShowModel(
        available_markets=[],
        copyrights=[],
        description="Example description",
        html_description="<p>Example description</p>",
        explicit=True,
        external_urls=ExternalUrlsModel(),
        href="https://api.spotify.com/v1/shows/44fyLyzKjE7ZAgy2t82CtD",  # type: ignore
        id="44fyLyzKjE7ZAgy2t82CtD",
        images=[],
        is_externally_hosted=False,
        languages=["pl"],
        media_type="audio",
        name="Example name",
        publisher=None,
        type="show",
        uri="spotify:show:44fyLyzKjE7ZAgy2t82CtD",
        total_episodes=111,
    )


@pytest.fixture
def example_simplified_episode_data():
    return SimplifiedEpisodeModel(
        audio_preview_url=None,
        description="Example description",
        html_description="<p>Example description</p>",
        duration_ms=10000,  # type: ignore
        explicit=True,
        external_urls=ExternalUrlsModel(),
        href="https://api.spotify.com/v1/episodes/44fyLyzKjE7ZAgy2t82CtD",  # type: ignore
        id="44fyLyzKjE7ZAgy2t82CtD",
        images=[],
        is_externally_hosted=False,
        is_playable=True,
        language="pl",
        languages=["pl"],
        name="Example name",
        release_date="2024-01-01",  # type: ignore
        release_date_precision="day",
        resume_point=None,
        type="episode",
        uri="spotify:episode:44fyLyzKjE7ZAgy2t82CtD",
        restrictions=None,
    )


@pytest.fixture
def example_episode_data(example_simplified_episode_data, example_simplified_show_data):
    return EpisodeModel(
        **example_simplified_episode_data.model_dump(exclude={"duration"}),
        duration_ms=180000,  # type: ignore
        show=example_simplified_show_data,
    )


@pytest.fixture
def example_saved_episode_data(example_episode_data):
    return SavedEpisodeModel(
        added_at="2024-01-01T00:00:00Z",  # type: ignore
        episode=example_episode_data,
    )


@pytest.fixture
def example_device_data():
    return DeviceModel(
        id="device_id",
        is_active=True,
        is_private_session=False,
        is_restricted=False,
        name="device_name",
        volume_percent=100,
        supports_volume=True,
        type="device_type",
    )


@pytest.fixture
def example_currently_playing_item_data(example_track_data):
    return CurrentlyPlayingItemModel(
        context=None,
        timestamp=datetime.now(),
        progress_ms=10000,  # type: ignore
        is_playing=True,
        currently_playing_type="track",  # type: ignore
        item=example_track_data,
        actions=PlaybackActionsModel(),
    )


@pytest.fixture
def example_playback_state_data(example_currently_playing_item_data, example_device_data, example_track_data):
    return PlaybackStateModel(
        **example_currently_playing_item_data.model_dump(exclude={"progress", "item"}),
        item=example_track_data,
        progress_ms=180000,  # type: ignore
        device=example_device_data,
        repeat_state="off",  # type: ignore
        shuffle_state=False,
        smart_shuffle=None,
    )


@pytest.fixture
def example_play_history_data(example_track_data):
    return PlayHistoryModel(
        track=example_track_data,
        played_at=datetime.now(),
        context=None,
    )


@pytest.fixture
def example_saved_show_data(example_simplified_show_data):
    return SavedShowModel(
        added_at="2024-01-01T00:00:00Z",  # type: ignore
        show=example_simplified_show_data,
    )


@pytest.fixture
def example_saved_track_data(example_track_data):
    return SavedTrackModel(
        added_at="2024-01-01T00:00:00Z",  # type: ignore
        track=example_track_data,
    )


@pytest.fixture
def example_playlist_owner_data():
    return PlaylistOwnerModel(
        external_urls=ExternalUrlsModel(),
        href="https://api.spotify.com/v1/users/44fyLyzKjE7ZAgy2t82CtD",  # type: ignore
        id="44fyLyzKjE7ZAgy2t82CtD",
        type="user",
        uri="spotify:user:44fyLyzKjE7ZAgy2t82CtD",
        display_name="user name",
    )


@pytest.fixture
def example_playlist_data(example_playlist_owner_data, example_track_data):
    return PlaylistModel(
        collaborative=True,
        description="example description",
        external_urls=ExternalUrlsModel(),
        href="https://api.spotify.com/v1/playlists/44fyLyzKjE7ZAgy2t82CtD",  # type: ignore
        id="44fyLyzKjE7ZAgy2t82CtD",
        images=None,
        name="example name",
        owner=example_playlist_owner_data,
        public=True,
        snapshot_id="snapshotID",
        type="playlist",
        uri="spotify:playlist:44fyLyzKjE7ZAgy2t82CtD",
        items=PagedResultModel(
            items=[
                PlaylistTrackModel(
                    added_at="2024-01-01T00:00:00Z",  # type: ignore
                    added_by=example_playlist_owner_data,
                    is_local=False,
                    item=example_track_data,
                )
            ],
            total=1,
            limit=1,
            offset=0,
            href="https://api.spotify.com/v1/playlist/4LOrSSPct7B6yCzW1IltRd/tracks",  # type: ignore
            next=None,
            previous=None,
        ),
    )


@pytest.fixture
def example_simplified_playlist_data(example_playlist_owner_data):
    return SimplifiedPlaylistModel(
        collaborative=True,
        description="example description",
        external_urls=ExternalUrlsModel(),
        href="https://api.spotify.com/v1/playlists/44fyLyzKjE7ZAgy2t82CtD",  # type: ignore
        id="44fyLyzKjE7ZAgy2t82CtD",
        images=None,
        name="example name",
        owner=example_playlist_owner_data,
        public=True,
        snapshot_id="snapshotID",
        type="playlist",
        uri="spotify:playlist:44fyLyzKjE7ZAgy2t82CtD",
        tracks=PlaylistSummaryModel(
            href="https://api.spotify.com/v1/tracks/44fyLyzKjE7ZAgy2t82CtD",  # type: ignore
            total=1,
        ),
    )


@pytest.fixture
def example_playlist_track_data(example_playlist_owner_data, example_track_data):
    return PlaylistTrackModel(
        added_at="2024-01-01T00:00:00Z",  # type: ignore
        added_by=example_playlist_owner_data,
        is_local=False,
        item=example_track_data,
    )
