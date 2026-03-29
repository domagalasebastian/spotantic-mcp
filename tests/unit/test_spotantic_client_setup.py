"""Unit tests for spotantic client setup and configuration."""

import os
from unittest.mock import patch

import pytest

from spotantic_mcp._spotantic_client._auth_managers import AuthMethod
from spotantic_mcp._spotantic_client._create_spotantic_client import get_access_token_info
from spotantic_mcp._spotantic_client._create_spotantic_client import get_auth_method
from spotantic_mcp._spotantic_client._create_spotantic_client import get_auth_settings


class TestGetAuthSettings:
    """Test the get_auth_settings function."""

    def test_get_auth_settings_with_all_env_vars(self) -> None:
        """Test reading auth settings when all environment variables are set."""
        with patch.dict(
            os.environ,
            {
                "SPOTANTIC_AUTH_CLIENT_ID": "test_client_id",
                "SPOTANTIC_AUTH_CLIENT_SECRET": "test_client_secret",
                "SPOTANTIC_AUTH_SCOPE": "user-read-private user-read-email",
                "SPOTANTIC_AUTH_STORE_ACCESS_TOKEN": "true",
            },
        ):
            settings = get_auth_settings()

            assert settings.client_id is not None
            assert settings.client_id.get_secret_value() == "test_client_id"
            assert settings.client_secret is not None
            assert settings.client_secret.get_secret_value() == "test_client_secret"
            assert settings.scope == "user-read-private user-read-email"
            assert settings.store_access_token is False

    def test_get_auth_settings_without_optional_vars(self) -> None:
        """Test that auth settings handle missing optional environment variables."""
        with patch.dict(os.environ, {}, clear=True):
            settings = get_auth_settings()

            assert settings.client_id is None
            assert settings.client_secret is None
            assert settings.scope is None
            assert settings.store_access_token is False

    def test_get_auth_settings_partial_vars(self) -> None:
        """Test auth settings with only some environment variables set."""
        with patch.dict(os.environ, {"SPOTANTIC_AUTH_CLIENT_ID": "test_id"}, clear=True):
            settings = get_auth_settings()

            assert settings.client_id is not None
            assert settings.client_id.get_secret_value() == "test_id"
            assert settings.client_secret is None


class TestGetAuthMethod:
    """Test the get_auth_method function."""

    def test_get_auth_method_client_credentials(self) -> None:
        """Test reading CLIENT_CREDENTIALS auth method."""
        with patch.dict(os.environ, {"SPOTANTIC_MCP_AUTH_METHOD": "client_credentials"}):
            method = get_auth_method()
            assert method == AuthMethod.CLIENT_CREDENTIALS

    def test_get_auth_method_auth_code(self) -> None:
        """Test reading AUTH_CODE auth method."""
        with patch.dict(os.environ, {"SPOTANTIC_MCP_AUTH_METHOD": "auth_code"}):
            method = get_auth_method()
            assert method == AuthMethod.AUTH_CODE

    def test_get_auth_method_auth_code_pkce(self) -> None:
        """Test reading AUTH_CODE_PKCE auth method."""
        with patch.dict(os.environ, {"SPOTANTIC_MCP_AUTH_METHOD": "auth_code_pkce"}):
            method = get_auth_method()
            assert method == AuthMethod.AUTH_CODE_PKCE

    def test_get_auth_method_case_insensitive(self) -> None:
        """Test that auth method is case-insensitive."""
        with patch.dict(os.environ, {"SPOTANTIC_MCP_AUTH_METHOD": "CLIENT_CREDENTIALS"}):
            method = get_auth_method()
            assert method == AuthMethod.CLIENT_CREDENTIALS

    def test_get_auth_method_missing_env_var(self) -> None:
        """Test that missing environment variable raises ValueError with helpful message."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="SPOTANTIC_MCP_AUTH_METHOD environment variable must be set"):
                get_auth_method()

    def test_get_auth_method_invalid_value(self) -> None:
        """Test that invalid auth method raises ValueError."""
        with patch.dict(os.environ, {"SPOTANTIC_MCP_AUTH_METHOD": "invalid_method"}):
            with pytest.raises(ValueError, match="Invalid authentication method"):
                get_auth_method()


class TestGetAccessTokenInfo:
    """Test the get_access_token_info function."""

    def test_get_access_token_info_with_refresh_token(self) -> None:
        """Test reading access token info when refresh token is set."""
        with patch.dict(os.environ, {"SPOTANTIC_MCP_REFRESH_TOKEN": "test_refresh_token"}):
            token_info = get_access_token_info()

            assert token_info.access_token.get_secret_value() == ""
            assert token_info.token_type == "Bearer"
            assert token_info.expires_in == 0
            assert token_info.refresh_token is not None
            assert token_info.refresh_token.get_secret_value() == "test_refresh_token"

    def test_get_access_token_info_without_refresh_token(self) -> None:
        """Test reading access token info when refresh token is not set."""
        with patch.dict(os.environ, {}, clear=True):
            token_info = get_access_token_info()

            assert token_info.access_token.get_secret_value() == ""
            assert token_info.token_type == "Bearer"
            assert token_info.expires_in == 0
            assert token_info.refresh_token is None

    def test_get_access_token_info_initial_token_empty(self) -> None:
        """Test that initial access token is intentionally empty."""
        # This documents that empty token is expected to be filled on auth/refresh
        with patch.dict(os.environ, {}, clear=True):
            token_info = get_access_token_info()
            # Empty token is expected - will be populated during authorization
            assert token_info.access_token.get_secret_value() == ""
