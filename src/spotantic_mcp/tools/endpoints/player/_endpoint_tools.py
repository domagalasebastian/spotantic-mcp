from spotantic_mcp.tools._tool_group import ToolGroup
from spotantic_mcp.tools._tool_types import EndpointTool

from ._add_item_to_playback_queue import add_item_to_playback_queue_tool
from ._get_available_devices import get_available_devices_tool
from ._get_currently_playing_track import get_currently_playing_track_tool
from ._get_playback_state import get_playback_state_tool
from ._get_recently_played_tracks import get_recently_played_tracks_tool
from ._get_user_queue import get_user_queue_tool
from ._pause_playback import pause_playback_tool
from ._seek_to_position import seek_to_position_tool
from ._set_playback_volume import set_playback_volume_tool
from ._set_repeat_mode import set_repeat_mode_tool
from ._skip_to_next import skip_to_next_tool
from ._skip_to_previous import skip_to_previous_tool
from ._start_resume_playback import start_resume_playback_tool
from ._toggle_playback_shuffle import toggle_playback_shuffle_tool
from ._transfer_playback import transfer_playback_tool

player_endpoint_tools = ToolGroup[EndpointTool](
    name="Spotify Player Endpoint Tools",
    tools=[
        add_item_to_playback_queue_tool,
        get_available_devices_tool,
        get_currently_playing_track_tool,
        get_playback_state_tool,
        get_recently_played_tracks_tool,
        get_user_queue_tool,
        pause_playback_tool,
        seek_to_position_tool,
        set_playback_volume_tool,
        set_repeat_mode_tool,
        skip_to_next_tool,
        skip_to_previous_tool,
        start_resume_playback_tool,
        toggle_playback_shuffle_tool,
        transfer_playback_tool,
    ],
)
