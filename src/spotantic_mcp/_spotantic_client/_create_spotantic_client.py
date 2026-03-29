import os

from pydantic import SecretStr
from spotantic.client import SpotanticClient
from spotantic.models.auth import AccessTokenInfo
from spotantic.models.auth import AuthSettings

from ._auth_managers import AuthManagerFactory
from ._auth_managers import AuthMethod


async def create_spotantic_client() -> SpotanticClient:
    """Set up the Spotantic client with authentication.

    This function reads authentication settings from environment variables, determines the authentication method to use,
    creates the appropriate authentication manager, and initializes the Spotantic client with the authenticated manager.

    Returns:
        An instance of SpotanticClient that is authenticated and ready to use.
    """
    auth_settings = get_auth_settings()
    auth_method = get_auth_method()
    access_token_info = get_access_token_info()

    auth_manager = await AuthManagerFactory.create_manager(auth_method, auth_settings, access_token_info)

    check_insufficient_scope = auth_settings.scope is not None
    client = SpotanticClient(
        auth_manager=auth_manager, max_attempts=3, check_insufficient_scope=check_insufficient_scope
    )

    return client


def get_auth_settings() -> AuthSettings:
    """Read authentication settings from environment variables.

    Returns:
        The authentication settings for the Spotantic client.
    """
    client_id = os.getenv("SPOTANTIC_AUTH_CLIENT_ID")
    client_secret = os.getenv("SPOTANTIC_AUTH_CLIENT_SECRET")
    auth_settings = AuthSettings(
        client_id=SecretStr(client_id) if client_id else None,
        client_secret=SecretStr(client_secret) if client_secret else None,
        scope=os.getenv("SPOTANTIC_AUTH_SCOPE"),
        store_access_token=False,
    )

    return auth_settings


def get_auth_method() -> AuthMethod:
    """Get the authentication method from environment variables.

    Returns:
        The authentication method to use for the Spotantic client.

    Raises:
        ValueError: If the SPOTANTIC_MCP_AUTH_METHOD environment variable is not set or is invalid.
    """
    auth_method_env = os.getenv("SPOTANTIC_MCP_AUTH_METHOD")
    if auth_method_env is None:
        raise ValueError(
            f"SPOTANTIC_MCP_AUTH_METHOD environment variable must be set. "
            f"Supported methods are: {[method.value for method in AuthMethod]}"
        )
    try:
        auth_method = AuthMethod(auth_method_env.lower())
    except ValueError:
        raise ValueError(
            f"Invalid authentication method: {auth_method_env}. "
            f"Supported methods are: {[method.value for method in AuthMethod]}"
        )

    return auth_method


def get_access_token_info() -> AccessTokenInfo:
    """Read access token information from environment variables.

    Returns:
        The access token information for the Spotantic client.
    """
    refresh_token = os.getenv("SPOTANTIC_MCP_REFRESH_TOKEN")

    return AccessTokenInfo(
        # Empty initial access token - will be populated on first authorization/refresh
        access_token=SecretStr(""),
        token_type="Bearer",
        expires_in=0,
        refresh_token=SecretStr(refresh_token) if refresh_token else None,
    )
