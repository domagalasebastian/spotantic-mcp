from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from spotantic.endpoints.player import get_available_devices

from spotantic_mcp._app_context import AppContext
from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import DeviceView


@handle_spotantic_errors
async def get_available_devices_tool(ctx: Context[ServerSession, AppContext]) -> list[DeviceView]:
    """Get information about a user’s available Spotify Connect devices.

    Some device models are not supported and will not be listed in the API response.

    Args:
        ctx: The tool context, which includes the server session and application context.

    Returns:
        A list of DeviceView objects containing information about the devices.
    """
    spotantic_client = ctx.request_context.lifespan_context.client
    api_data = (await get_available_devices(spotantic_client)).data

    return [DeviceView.model_validate(device) for device in api_data]
