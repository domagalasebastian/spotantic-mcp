import argparse
import asyncio

from spotantic.auth import AuthCodeFlowManager
from spotantic.auth import AuthCodePKCEFlowManager
from spotantic.auth import ClientCredentialsFlowManager
from spotantic.models.auth import AuthSettings


async def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an access token using the specified authentication method.")
    parser.add_argument(
        "--auth-method",
        choices=["code-pkce", "cc", "code"],
        default="code-pkce",
        help="The authentication method to use.",
    )
    args = parser.parse_args()

    auth_settings = AuthSettings(store_access_token=True)
    if args.auth_method == "code-pkce":
        auth_manager = AuthCodePKCEFlowManager(auth_settings=auth_settings)
    elif args.auth_method == "code":
        auth_manager = AuthCodeFlowManager(auth_settings=auth_settings)
    elif args.auth_method == "cc":
        auth_manager = ClientCredentialsFlowManager(auth_settings=auth_settings)
    else:
        raise ValueError(f"Unsupported authentication method: {args.auth_method}")

    await auth_manager.authorize()


if __name__ == "__main__":
    asyncio.run(main())
