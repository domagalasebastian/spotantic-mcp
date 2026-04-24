from pydantic import Field
from pydantic import HttpUrl

from ._base_view import BaseView


class PlaylistSummaryView(BaseView):
    """Model representing information to retrieve full details of the playlist's tracks."""

    tracks_href: HttpUrl = Field(
        alias="href",
        description="A link to the Web API endpoint where full details of the playlist's tracks can be retrieved.",
    )
    """A link to the Web API endpoint where full details of the playlist's tracks can be retrieved."""

    tracks_total: int = Field(alias="total", description="Number of tracks in the playlist.")
    """Number of tracks in the playlist."""
