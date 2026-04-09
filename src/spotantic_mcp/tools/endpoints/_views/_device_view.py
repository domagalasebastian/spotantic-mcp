from pydantic import Field

from ._base_view import BaseView


class DeviceView(BaseView):
    """Model representing information about an user’s Spotify Connect device."""

    device_id: str | None = Field(
        None,
        alias="id",
        description="The device ID. This ID is unique and persistent to some extent.",
    )
    """The device ID. This ID is unique and persistent to some extent."""

    is_active: bool = Field(description="If this device is the currently active device.")
    """If this device is the currently active device."""

    is_private_session: bool = Field(repr=False, description="If this device is currently in a private session.")
    """If this device is currently in a private session."""

    is_restricted: bool = Field(
        description=(
            "Whether controlling this device is restricted. At present if this is `True` then "
            "no Web API commands will be accepted by this device."
        )
    )
    """Whether controlling this device is restricted. At present if this is `True` then
    no Web API commands will be accepted by this device."""

    device_name: str = Field(alias="name", description="A human-readable name for the device.")
    """A human-readable name for the device."""

    device_type: str = Field(alias="type", description="A device type.")
    """A device type."""

    volume_percent: int | None = Field(None, description="The current volume in percent.")
    """The current volume in percent."""

    supports_volume: bool = Field(description="If this device can be used to set the volume.")
    """If this device can be used to set the volume."""
