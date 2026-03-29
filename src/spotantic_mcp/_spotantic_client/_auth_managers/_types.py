from enum import StrEnum

from spotantic.auth import AuthCodeFlowManager
from spotantic.auth import AuthCodePKCEFlowManager
from spotantic.auth import ClientCredentialsFlowManager

type AuthManager = AuthCodeFlowManager | AuthCodePKCEFlowManager | ClientCredentialsFlowManager
"""A type alias for the authentication manager types."""


class AuthMethod(StrEnum):
    """Enumeration of supported authentication methods for the Spotantic client."""

    CLIENT_CREDENTIALS = "client_credentials"
    """Client Credentials Flow authentication method."""

    AUTH_CODE = "auth_code"
    """Authorization Code Flow authentication method."""

    AUTH_CODE_PKCE = "auth_code_pkce"
    """Authorization Code PKCE Flow authentication method."""
