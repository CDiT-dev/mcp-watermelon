"""Authentication for the MCP server.

Uses OIDCProxy to proxy the OAuth flow to Keycloak using pre-registered
client credentials. Claude.ai (and Claude Code through it) authenticates
via the standard authorization_code flow.
"""

import logging

from fastmcp.server.auth.oidc_proxy import OIDCProxy

logger = logging.getLogger(__name__)


def build_auth(
    base_url: str,
    keycloak_issuer: str,
    keycloak_client_id: str,
    keycloak_client_secret: str,
) -> OIDCProxy | None:
    """Build the OIDCProxy authentication provider.

    Returns None if the client secret is empty.
    """
    if not keycloak_client_secret:
        logger.warning(
            "KEYCLOAK_CLIENT_SECRET is empty — OIDC auth disabled"
        )
        return None

    config_url = f"{keycloak_issuer}/.well-known/openid-configuration"
    return OIDCProxy(
        config_url=config_url,
        client_id=keycloak_client_id,
        client_secret=keycloak_client_secret,
        base_url=base_url,
    )
