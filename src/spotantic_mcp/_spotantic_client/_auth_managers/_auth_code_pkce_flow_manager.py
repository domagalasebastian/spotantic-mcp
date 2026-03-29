from spotantic.auth import AuthCodePKCEFlowManager
from spotantic.models.auth import AccessTokenInfo
from spotantic.models.auth import AuthSettings

from ._auth_manager_factory import AuthManagerFactory
from ._types import AuthMethod


@AuthManagerFactory.register_decorator(AuthMethod.AUTH_CODE_PKCE)
async def create_auth_code_pkce_manager(
    auth_settings: AuthSettings, access_token_info: AccessTokenInfo
) -> AuthCodePKCEFlowManager:
    """Create an Authorization Code PKCE Flow authentication manager.

    Args:
        auth_settings: The authentication settings to use for creating the manager.
        access_token_info: The access token information to use for creating the manager.

    Returns:
        An instance of AuthCodePKCEFlowManager that is authenticated based on the settings and access token information.

    Raises:
        ValueError: If the client ID is not provided in the authentication settings or
         if the access token information does not contain a refresh token.
    """
    if auth_settings.client_id is None:
        raise ValueError("Client ID must be set for Authorization Code PKCE Flow")

    if access_token_info.refresh_token is None:
        raise ValueError("Refresh token must be set for creating an Authorization Code PKCE Flow manager")

    auth_manager = AuthCodePKCEFlowManager(
        auth_settings=auth_settings, access_token_info=access_token_info, allow_lazy_refresh=True
    )
    await auth_manager.refresh()

    return auth_manager
