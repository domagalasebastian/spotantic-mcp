from spotantic.auth import AuthCodeFlowManager
from spotantic.models.auth import AccessTokenInfo
from spotantic.models.auth import AuthSettings

from ._auth_manager_factory import AuthManagerFactory
from ._types import AuthMethod


@AuthManagerFactory.register_decorator(AuthMethod.AUTH_CODE)
async def create_auth_code_manager(
    auth_settings: AuthSettings, access_token_info: AccessTokenInfo
) -> AuthCodeFlowManager:
    """Create an Authorization Code Flow authentication manager.

    Args:
        auth_settings: The authentication settings to use for creating the manager.
        access_token_info: The access token information to use for creating the manager.

    Returns:
        An instance of AuthCodeFlowManager that is authenticated based on the settings and access token information.

    Raises:
        ValueError: If the client ID or client secret is not provided in the authentication settings or
         if the access token information does not contain a refresh token.
    """
    if auth_settings.client_id is None:
        raise ValueError("Client ID must be set for Authorization Code Flow")

    if auth_settings.client_secret is None:
        raise ValueError("Client Secret must be set for Authorization Code Flow")

    if access_token_info.refresh_token is None:
        raise ValueError("Refresh token must be set for creating an Authorization Code Flow manager")

    auth_manager = AuthCodeFlowManager(
        auth_settings=auth_settings, access_token_info=access_token_info, allow_lazy_refresh=True
    )
    await auth_manager.refresh()

    return auth_manager
