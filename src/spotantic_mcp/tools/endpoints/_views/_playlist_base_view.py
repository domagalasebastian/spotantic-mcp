from pydantic import Field
from spotantic.types import SpotifyItemID

from ._base_view import BaseView
from ._user_view import UserView


class PlaylistBaseView(BaseView):
    """Model containing common fields for playlist objects."""

    collaborative: bool = Field(
        repr=False, description="`True` if the owner allows other users to modify the playlist."
    )
    """`True` if the owner allows other users to modify the playlist."""

    description: str | None = Field(None, description="The playlist description.")
    """The playlist description."""

    playlist_id: SpotifyItemID = Field(alias="id", repr=False, description="The Spotify ID for the playlist.")
    """The Spotify ID for the playlist."""

    playlist_name: str = Field(alias="name", description="The name of the playlist.")
    """The name of the playlist."""

    owner: UserView = Field(description="The user who owns the playlist.")
    """The user who owns the playlist."""

    public: bool | None = Field(
        None,
        repr=False,
        description=(
            "`True` the playlist is public, `False` the playlist is private, "
            "`None` the playlist status is not relevant."
        ),
    )
    """`True` the playlist is public, `False` the playlist is private, `None` the playlist status is not relevant."""

    snapshot_id: str = Field(
        description=(
            "The version identifier for the current playlist. Can be supplied in other requests to "
            "target a specific playlist version."
        )
    )
    """The version identifier for the current playlist.
    Can be supplied in other requests to target a specific playlist version."""
