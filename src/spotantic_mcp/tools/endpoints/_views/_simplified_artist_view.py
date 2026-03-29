from pydantic import Field
from spotantic.types import SpotifyItemID

from ._base_view import BaseView


class SimplifiedArtistView(BaseView):
    """Model representing simplified Spotify catalog information for a single artist."""

    artist_id: SpotifyItemID = Field(alias="id", repr=False, description="The Spotify ID for the artist.")
    """The Spotify ID for the artist."""

    artist_name: str = Field(alias="name", description="The name of the artist.")
    """The name of the artist."""
