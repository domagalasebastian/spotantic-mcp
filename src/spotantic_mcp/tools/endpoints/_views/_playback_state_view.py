from pydantic import Field
from spotantic.types import RepeatMode

from ._currently_playing_item_view import CurrentlyPlayingItemView
from ._device_view import DeviceView


class PlaybackStateView(CurrentlyPlayingItemView):
    """Model representing the playback state."""

    device: DeviceView = Field(description="The device that is currently active.")
    """The device that is currently active."""

    repeat_state: RepeatMode = Field(description="off, track, context")
    """off, track, context"""

    shuffle_state: bool = Field(description="If shuffle is on or off.")
    """If shuffle is on or off."""

    smart_shuffle: bool | None = Field(None, description="If smart shuffle is on or off.")
    """If smart shuffle is on or off."""
