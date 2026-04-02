"""Keycloak OIDC + Bearer token authentication for Watermelon MCP.

Supports two authentication modes simultaneously via MultiAuth:

1. **Keycloak OIDC** (for Claude.ai connectors and other OAuth clients):
   The server proxies the full OAuth flow via OIDCProxy using pre-registered
   Keycloak client credentials. No Dynamic Client Registration (DCR) needed.

2. **Bearer token** (for Claude Code, n8n, and other direct clients):
   Simple static API key validation via Authorization: Bearer <key>.
"""

import hmac
import logging

from fastmcp.server.auth import (
    AccessToken,
    MultiAuth,
    TokenVerifier,
)
from fastmcp.server.auth.oidc_proxy import OIDCProxy

logger = logging.getLogger(__name__)


class BearerTokenVerifier(TokenVerifier):
    """Validates static API key via constant-time comparison."""

    def __init__(self, api_key: str):
        super().__init__()
        self._api_key = api_key

    async def verify_token(self, token: str) -> AccessToken | None:
        if not hmac.compare_digest(token, self._api_key):
            return None
        return AccessToken(token=token, client_id="watermelon-bearer", scopes=["all"])


def build_auth(
    keycloak_issuer: str,
    keycloak_client_id: str,
    keycloak_client_secret: str,
    base_url: str,
    api_key: str = "",
) -> MultiAuth | None:
    """Create Keycloak OIDC auth with optional bearer token fallback.

    Returns a MultiAuth that accepts both:
    - Keycloak OIDC clients (Claude.ai) via OIDCProxy (server-side OAuth)
    - Bearer token clients (Claude Code, n8n) via static API key

    Args:
        keycloak_issuer: Keycloak realm issuer URL.
        keycloak_client_id: Pre-registered Keycloak client ID.
        keycloak_client_secret: Keycloak client secret.
        base_url: Public URL of this server.
        api_key: Static API key for bearer token auth (empty to skip).
    """
    if not keycloak_client_secret:
        logger.warning(
            "KEYCLOAK_CLIENT_SECRET is empty — OIDC auth disabled"
        )
        return None

    config_url = f"{keycloak_issuer}/.well-known/openid-configuration"

    oidc_auth = OIDCProxy(
        config_url=config_url,
        client_id=keycloak_client_id,
        client_secret=keycloak_client_secret,
        base_url=base_url,
    )

    verifiers: list[TokenVerifier] = []
    if api_key:
        verifiers.append(BearerTokenVerifier(api_key))

    return MultiAuth(server=oidc_auth, verifiers=verifiers)
