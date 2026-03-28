from spotantic.auth import ClientCredentialsFlowManager
from spotantic.models.auth import AccessTokenInfo
from spotantic.models.auth import AuthSettings

from ._auth_manager_factory import AuthManagerFactory
from ._types import AuthMethod


@AuthManagerFactory.register_decorator(AuthMethod.CLIENT_CREDENTIALS)
async def create_client_credentials_manager(
    auth_settings: AuthSettings, access_token_info: AccessTokenInfo
) -> ClientCredentialsFlowManager:
    """Create a Client Credentials Flow authentication manager.

    Args:
        auth_settings: The authentication settings to use for creating the manager.
        access_token_info: The access token information to use for creating the manager.

    Returns:
        An instance of ClientCredentialsFlowManager that is authenticated based on
        the settings and access token information.

    Raises:
        ValueError: If the client ID or client secret is not provided in the authentication settings.
    """
    if auth_settings.client_id is None:
        raise ValueError("Client ID must be set for Client Credentials Flow")

    if auth_settings.client_secret is None:
        raise ValueError("Client Secret must be set for Client Credentials Flow")

    auth_manager = ClientCredentialsFlowManager(auth_settings=auth_settings, access_token_info=access_token_info)
    await auth_manager.authorize()

    return auth_manager
