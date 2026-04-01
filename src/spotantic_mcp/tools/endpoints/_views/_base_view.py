from pydantic import BaseModel
from pydantic import ConfigDict


class BaseView(BaseModel):
    """Base class for all Spotify MCP View models."""

    model_config = ConfigDict(
        serialize_by_alias=True, populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True
    )
