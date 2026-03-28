from typing import Awaitable
from typing import Callable

from spotantic.models.auth import AccessTokenInfo
from spotantic.models.auth import AuthSettings

from ._types import AuthManager
from ._types import AuthMethod


class AuthManagerFactory:
    """Factory for creating authentication managers based on the specified authentication method."""

    _REGISTRY = {}

    @classmethod
    def register(
        cls, auth_method: AuthMethod, manager_creator: Callable[[AuthSettings, AccessTokenInfo], Awaitable[AuthManager]]
    ) -> None:
        """Register an authentication manager class for a specific authentication method.

        Args:
            auth_method: The authentication method to register the manager for.
            manager_creator: A function that creates an instance of the authentication manager.

        Raises:
            ValueError: If the authentication method is already registered or
             if the manager class is not a subclass of AuthManager.
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
            auth_method: The authentication method to register the manager for.

        Returns:
            A decorator function that registers the decorated authentication manager class for
             the specified authentication method.
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
            auth_method: The authentication method to create the manager for.
            auth_settings: The authentication settings to use for creating the manager.
            access_token_info: The access token information to use for creating the manager.

        Returns:
            An instance of AuthManager that is authenticated based on the specified authentication method.

        Raises:
            ValueError: If the authentication method is not registered or
             if the created manager is not an instance of AuthManager.
        """
        if auth_method not in cls._REGISTRY:
            raise ValueError(
                f"Authentication method {auth_method} is not registered. "
                f"Supported methods are: {list(cls._REGISTRY.keys())}"
            )

        manager_creator = cls._REGISTRY[auth_method]
        manager = await manager_creator(auth_settings, access_token_info)

        return manager
