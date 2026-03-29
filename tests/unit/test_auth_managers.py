"""Unit tests for authentication manager factory and individual managers."""

import pytest
from pydantic import SecretStr
from spotantic.models.auth import AccessTokenInfo
from spotantic.models.auth import AuthSettings

from spotantic_mcp._spotantic_client._auth_managers import AuthManagerFactory
from spotantic_mcp._spotantic_client._auth_managers import AuthMethod
from spotantic_mcp._spotantic_client._auth_managers import create_auth_code_manager
from spotantic_mcp._spotantic_client._auth_managers import create_auth_code_pkce_manager
from spotantic_mcp._spotantic_client._auth_managers import create_client_credentials_manager


class TestAuthMethod:
    """Test the AuthMethod enum."""

    def test_auth_method_values(self) -> None:
        """Test that AuthMethod enum has expected values."""
        assert AuthMethod.CLIENT_CREDENTIALS.value == "client_credentials"
        assert AuthMethod.AUTH_CODE.value == "auth_code"
        assert AuthMethod.AUTH_CODE_PKCE.value == "auth_code_pkce"

    def test_auth_method_from_string(self) -> None:
        """Test creating AuthMethod from string values."""
        assert AuthMethod("client_credentials") == AuthMethod.CLIENT_CREDENTIALS
        assert AuthMethod("auth_code") == AuthMethod.AUTH_CODE
        assert AuthMethod("auth_code_pkce") == AuthMethod.AUTH_CODE_PKCE

    def test_auth_method_invalid_value(self) -> None:
        """Test that invalid AuthMethod values raise ValueError."""
        with pytest.raises(ValueError):
            AuthMethod("invalid_method")


class TestAuthManagerFactory:
    """Test the AuthManagerFactory registry and factory methods."""

    def test_factory_has_registered_methods(self) -> None:
        """Test that all auth methods are registered in the factory."""
        # The registry should contain all three auth methods after imports
        assert AuthMethod.CLIENT_CREDENTIALS in AuthManagerFactory._REGISTRY
        assert AuthMethod.AUTH_CODE in AuthManagerFactory._REGISTRY
        assert AuthMethod.AUTH_CODE_PKCE in AuthManagerFactory._REGISTRY

    def test_registry_register_duplicate_raises_error(self) -> None:
        """Test that registering a duplicate auth method raises ValueError."""
        # Try to register an already registered method
        with pytest.raises(ValueError, match="already registered"):
            AuthManagerFactory.register(AuthMethod.CLIENT_CREDENTIALS, create_client_credentials_manager)


class TestClientCredentialsManager:
    """Test the Client Credentials Flow manager creation."""

    @pytest.mark.asyncio
    async def test_create_client_credentials_manager_missing_client_id(self) -> None:
        """Test that missing client ID raises ValueError."""
        auth_settings = AuthSettings(
            client_id=None,
            client_secret=SecretStr("test_secret"),
        )
        access_token_info = AccessTokenInfo(
            access_token=SecretStr("test_token"),
            token_type="Bearer",
            expires_in=3600,
        )

        with pytest.raises(ValueError, match="Client ID must be set"):
            await create_client_credentials_manager(auth_settings, access_token_info)

    @pytest.mark.asyncio
    async def test_create_client_credentials_manager_missing_client_secret(self) -> None:
        """Test that missing client secret raises ValueError."""
        auth_settings = AuthSettings(
            client_id=SecretStr("test_id"),
            client_secret=None,
        )
        access_token_info = AccessTokenInfo(
            access_token=SecretStr("test_token"),
            token_type="Bearer",
            expires_in=3600,
        )

        with pytest.raises(ValueError, match="Client Secret must be set"):
            await create_client_credentials_manager(auth_settings, access_token_info)


class TestAuthCodeFlowManager:
    """Test the Authorization Code Flow manager creation."""

    @pytest.mark.asyncio
    async def test_create_auth_code_manager_missing_client_id(self) -> None:
        """Test that missing client ID raises ValueError."""
        auth_settings = AuthSettings(
            client_id=None,
            client_secret=SecretStr("test_secret"),
        )
        access_token_info = AccessTokenInfo(
            access_token=SecretStr("test_token"),
            token_type="Bearer",
            expires_in=3600,
            refresh_token=SecretStr("test_refresh"),
        )

        with pytest.raises(ValueError, match="Client ID must be set"):
            await create_auth_code_manager(auth_settings, access_token_info)

    @pytest.mark.asyncio
    async def test_create_auth_code_manager_missing_client_secret(self) -> None:
        """Test that missing client secret raises ValueError."""
        auth_settings = AuthSettings(
            client_id=SecretStr("test_id"),
            client_secret=None,
        )
        access_token_info = AccessTokenInfo(
            access_token=SecretStr("test_token"),
            token_type="Bearer",
            expires_in=3600,
            refresh_token=SecretStr("test_refresh"),
        )

        with pytest.raises(ValueError, match="Client Secret must be set"):
            await create_auth_code_manager(auth_settings, access_token_info)

    @pytest.mark.asyncio
    async def test_create_auth_code_manager_missing_refresh_token(self) -> None:
        """Test that missing refresh token raises ValueError."""
        auth_settings = AuthSettings(
            client_id=SecretStr("test_id"),
            client_secret=SecretStr("test_secret"),
        )
        access_token_info = AccessTokenInfo(
            access_token=SecretStr("test_token"),
            token_type="Bearer",
            expires_in=3600,
            refresh_token=None,
        )

        with pytest.raises(ValueError, match="Refresh token must be set"):
            await create_auth_code_manager(auth_settings, access_token_info)


class TestAuthCodePKCEFlowManager:
    """Test the Authorization Code PKCE Flow manager creation."""

    @pytest.mark.asyncio
    async def test_create_auth_code_pkce_manager_missing_client_id(self) -> None:
        """Test that missing client ID raises ValueError."""
        auth_settings = AuthSettings(
            client_id=None,
        )
        access_token_info = AccessTokenInfo(
            access_token=SecretStr("test_token"),
            token_type="Bearer",
            expires_in=3600,
            refresh_token=SecretStr("test_refresh"),
        )

        with pytest.raises(ValueError, match="Client ID must be set"):
            await create_auth_code_pkce_manager(auth_settings, access_token_info)

    @pytest.mark.asyncio
    async def test_create_auth_code_pkce_manager_missing_refresh_token(self) -> None:
        """Test that missing refresh token raises ValueError."""
        auth_settings = AuthSettings(
            client_id=SecretStr("test_id"),
        )
        access_token_info = AccessTokenInfo(
            access_token=SecretStr("test_token"),
            token_type="Bearer",
            expires_in=3600,
            refresh_token=None,
        )

        with pytest.raises(ValueError, match="Refresh token must be set"):
            await create_auth_code_pkce_manager(auth_settings, access_token_info)
