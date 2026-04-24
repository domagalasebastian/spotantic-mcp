from pydantic import Field

from ._base_view import BaseView


class UserView(BaseView):
    """Model representing public profile information about a Spotify user."""

    display_name: str | None = Field(None, description="The name displayed on the user's profile.")
    """The name displayed on the user's profile."""

    user_id: str = Field(alias="id", description="The Spotify user ID for the user.")
    """The Spotify user ID for the user."""
