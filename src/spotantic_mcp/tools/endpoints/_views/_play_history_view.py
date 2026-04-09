from datetime import datetime

from pydantic import Field
from spotantic.models.spotify.submodels import ContextModel

from ._base_view import BaseView
from ._track_view import TrackView


class PlayHistoryView(BaseView):
    """Model representing information about a play history."""

    track: TrackView = Field(description="The track the user listened to.")
    """The track the user listened to."""

    played_at: datetime = Field(description="The date and time the track was played.")
    """The date and time the track was played."""

    context: ContextModel | None = Field(None, description="The context the track was played from.")
    """The context the track was played from."""
