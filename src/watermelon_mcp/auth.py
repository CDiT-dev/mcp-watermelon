"""Keycloak JWT + Bearer token authentication for Watermelon MCP."""

import hmac

from fastmcp.server.auth import (
    AccessToken,
    JWTVerifier,
    MultiAuth,
    RemoteAuthProvider,
    TokenVerifier,
)


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
    keycloak_audience: str,
    base_url: str,
    api_key: str = "",
) -> MultiAuth:
    """Create Keycloak JWT auth with optional bearer token fallback."""
    jwks_uri = f"{keycloak_issuer.rstrip('/')}/protocol/openid-connect/certs"

    jwt_verifier = JWTVerifier(
        jwks_uri=jwks_uri,
        issuer=keycloak_issuer,
        audience=keycloak_audience,
    )

    keycloak_auth = RemoteAuthProvider(
        token_verifier=jwt_verifier,
        authorization_servers=[keycloak_issuer],
        base_url=base_url,
        scopes_supported=["openid"],
        resource_name="Watermelon MCP Server",
    )

    verifiers: list[TokenVerifier] = []
    if api_key:
        verifiers.append(BearerTokenVerifier(api_key))

    return MultiAuth(server=keycloak_auth, verifiers=verifiers)
