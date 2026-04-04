from pydantic import Field

from ._simplified_episode_view import SimplifiedEpisodeView
from ._simplified_show_view import SimplifiedShowView


class EpisodeView(SimplifiedEpisodeView):
    """Model representing catalog information for a single episode identified by its unique Spotify ID."""

    show: SimplifiedShowView = Field(description="The show on which the episode belongs.")
    """The show on which the episode belongs."""
