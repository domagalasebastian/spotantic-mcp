import os
from enum import StrEnum
from typing import Awaitable
from typing import Callable

from pydantic import SecretStr
from spotantic.auth import AuthCodeFlowManager
from spotantic.auth import AuthCodePKCEFlowManager
from spotantic.auth import ClientCredentialsFlowManager
from spotantic.client import SpotanticClient
from spotantic.models.auth import AccessTokenInfo
from spotantic.models.auth import AuthSettings

type AuthManager = AuthCodeFlowManager | AuthCodePKCEFlowManager | ClientCredentialsFlowManager


class AuthMethod(StrEnum):
    CLIENT_CREDENTIALS = "client_credentials"
    AUTH_CODE = "auth_code"
    AUTH_CODE_PKCE = "auth_code_pkce"


class AuthManagerFactory:
    """Factory for creating authentication managers based on the specified authentication method."""

    _REGISTRY = {}

    @classmethod
    def register(
        cls, auth_method: AuthMethod, manager_creator: Callable[[AuthSettings, AccessTokenInfo], Awaitable[AuthManager]]
    ) -> None:
        """Register an authentication manager class for a specific authentication method.

        Args:
            auth_method (AuthMethod): The authentication method to register the manager for.
            manager_creator (Callable[[AuthSettings, AccessTokenInfo], AuthManager]): A function that creates an instance of the authentication manager.

        Raises:
            ValueError: If the authentication method is already registered or if the manager class is not a subclass of AuthManager.
        """
        if auth_method in cls._REGISTRY:
            raise ValueError(
                f"Authentication method {auth_method} is already registered with manager {cls._REGISTRY[auth_method]}"
            )

        cls._REGISTRY[auth_method] = manager_creator

    @classmethod
    def register_decorator(
        cls, auth_method: AuthMethod
    ) -> Callable[
        [Callable[[AuthSettings, AccessTokenInfo], Awaitable[AuthManager]]],
        Callable[[AuthSettings, AccessTokenInfo], Awaitable[AuthManager]],
    ]:
        """Decorator to register an authentication manager class for a specific authentication method.

        Args:
            auth_method (AuthMethod): The authentication method to register the manager for.

        Returns:
            A decorator function that registers the decorated authentication manager class for the specified authentication method.
        """

        def decorator(
            manager_creator: Callable[[AuthSettings, AccessTokenInfo], Awaitable[AuthManager]],
        ) -> Callable[[AuthSettings, AccessTokenInfo], Awaitable[AuthManager]]:
            cls.register(auth_method, manager_creator)
            return manager_creator

        return decorator

    @classmethod
    async def create_manager(
        cls, auth_method: AuthMethod, auth_settings: AuthSettings, access_token_info: AccessTokenInfo
    ) -> AuthManager:
        """Create an authentication manager instance based on the specified authentication method.

        Args:
            auth_method (AuthMethod): The authentication method to create the manager for.
            auth_settings (AuthSettings): The authentication settings to use for creating the manager.
            access_token_info (AccessTokenInfo): The access token information to use for creating the manager.

        Returns:
            An instance of AuthManager that is authenticated based on the specified authentication method.

        Raises:
            ValueError: If the authentication method is not registered or if the created manager is not an instance of AuthManager.
        """
        if auth_method not in cls._REGISTRY:
            raise ValueError(
                f"Authentication method {auth_method} is not registered. Supported methods are: {list(cls._REGISTRY.keys())}"
            )

        manager_creator = cls._REGISTRY[auth_method]
        manager = await manager_creator(auth_settings, access_token_info)

        return manager


async def setup_spotantic_client() -> SpotanticClient:
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
        AuthSettings: The authentication settings for the Spotantic client.
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
        AuthMethod: The authentication method to use for the Spotantic client.

    Raises:
        ValueError: If the authentication method specified in the environment variable is invalid.
    """
    auth_method_env = os.getenv("SPOTANTIC_MCP_AUTH_METHOD")
    try:
        auth_method = AuthMethod(auth_method_env)
    except ValueError:
        raise ValueError(
            f"Invalid authentication method: {auth_method_env}. Supported methods are: {[method.value for method in AuthMethod]}"
        )

    return auth_method


def get_access_token_info() -> AccessTokenInfo:
    """Read access token information from environment variables.

    Returns:
        AccessTokenInfo: The access token information for the Spotantic client.
    """
    refresh_token = os.getenv("SPOTANTIC_AUTH_REFRESH_TOKEN")

    return AccessTokenInfo(
        access_token=SecretStr(""),
        token_type="Bearer",
        expires_in=0,
        refresh_token=SecretStr(refresh_token) if refresh_token else None,
    )


@AuthManagerFactory.register_decorator(AuthMethod.CLIENT_CREDENTIALS)
async def create_client_credentials_manager(
    auth_settings: AuthSettings, access_token_info: AccessTokenInfo
) -> ClientCredentialsFlowManager:
    """Create a Client Credentials Flow authentication manager based on the provided settings and access token information.

    Args:
        auth_settings (AuthSettings): The authentication settings to use for creating the manager.
        access_token_info (AccessTokenInfo): The access token information to use for creating the manager.

    Returns:
        An instance of ClientCredentialsFlowManager that is authenticated based on the settings and access token information.

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


@AuthManagerFactory.register_decorator(AuthMethod.AUTH_CODE)
async def create_auth_code_manager(
    auth_settings: AuthSettings, access_token_info: AccessTokenInfo
) -> AuthCodeFlowManager:
    """Create an Authorization Code Flow authentication manager based on the provided settings and access token information.

    Args:
        auth_settings (AuthSettings): The authentication settings to use for creating the manager.
        access_token_info (AccessTokenInfo): The access token information to use for creating the manager.

    Returns:
        An instance of AuthCodeFlowManager that is authenticated based on the settings and access token information.

    Raises:
        ValueError: If the client ID or client secret is not provided in the authentication settings or if the access token information does not contain a refresh token.
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


@AuthManagerFactory.register_decorator(AuthMethod.AUTH_CODE_PKCE)
async def create_auth_code_pkce_manager(
    auth_settings: AuthSettings, access_token_info: AccessTokenInfo
) -> AuthCodePKCEFlowManager:
    """Create an Authorization Code PKCE Flow authentication manager based on the provided settings and access token information.

    Args:
        auth_settings (AuthSettings): The authentication settings to use for creating the manager.
        access_token_info (AccessTokenInfo): The access token information to use for creating the manager.

    Returns:
        An instance of AuthCodePKCEFlowManager that is authenticated based on the settings and access token information.

    Raises:
        ValueError: If the client ID is not provided in the authentication settings or if the access token information does not contain a refresh token.
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
