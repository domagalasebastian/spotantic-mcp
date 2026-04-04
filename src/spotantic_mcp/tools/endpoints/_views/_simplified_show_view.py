from pydantic import Field
from spotantic.types import SpotifyItemID

from ._base_view import BaseView


class SimplifiedShowView(BaseView):
    """Model representing simplified Spotify catalog information for a single show."""

    description: str = Field(description="A description of the show.")
    """A description of the show. HTML tags are stripped away from this field."""

    show_id: SpotifyItemID = Field(alias="id", repr=False, description="The Spotify ID for the show.")
    """The Spotify ID for the show."""

    show_name: str = Field(alias="name", description="The name of the episode.")
    """The name of the episode."""

    total_episodes: int = Field(description="The total number of episodes in the show.")
    """The total number of episodes in the show."""
