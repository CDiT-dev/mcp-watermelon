"""Watermelon MCP Server entry point."""

import os
from datetime import datetime, timezone

from fastmcp import FastMCP
from mcp.types import Icon
from starlette.requests import Request
from starlette.responses import JSONResponse

from . import __version__
from .auth import BearerTokenVerifier
from .client import WatermelonClient
from .settings import get_settings
from .tools_contacts import register_contact_tools
from .tools_conversations import register_conversation_tools
from .tools_messages import register_message_tools
from .tools_fields import register_field_tools
from .tools_webhooks import register_webhook_tools

_start_time = datetime.now(timezone.utc)


def create_server() -> FastMCP:
    """Create and configure the FastMCP server with all tools."""
    settings = get_settings()
    client = WatermelonClient(settings.watermelon_api_key, settings.watermelon_secret_key)

    # Bearer token auth. Fail-fast in HTTP mode (no more silent unauth starts).
    _api_key = os.getenv("MCP_API_KEY", "")
    if settings.mcp_transport in ("http", "streamable-http") and not _api_key:
        raise SystemExit(
            "MCP_API_KEY is required in HTTP mode. Refusing to start "
            "an unauthenticated server."
        )
    auth = BearerTokenVerifier(api_key=_api_key) if _api_key else None

    mcp = FastMCP(
        "mcp-watermelon",
        auth=auth,
        icons=[
            Icon(
                src="https://watermelon.ai/favicons/logo.svg",
                mimeType="image/svg+xml",
            ),
        ],
    )

    register_contact_tools(mcp, client)
    register_conversation_tools(mcp, client)
    register_message_tools(mcp, client)
    register_field_tools(mcp, client)
    register_webhook_tools(mcp, client)

    @mcp.custom_route("/health", methods=["GET"])
    async def _health(request: Request) -> JSONResponse:
        return JSONResponse({
            "status": "healthy",
            "service": "mcp-watermelon",
            "version": __version__,
            "upstream_reachable": True,
            "uptime_seconds": int((datetime.now(timezone.utc) - _start_time).total_seconds()),
        })

    @mcp.custom_route("/healthz", methods=["GET"])
    async def _healthz(request: Request) -> JSONResponse:
        return await _health(request)

    return mcp


def main() -> None:
    """Main entry point — run the server with configured transport."""
    settings = get_settings()
    server = create_server()
    # Normalize transport + stateless_http for reliability
    transport = settings.mcp_transport
    if transport in ("http", "streamable-http"):
        server.run(
            transport="streamable-http",
            host=settings.mcp_host,
            port=settings.mcp_port,
            stateless_http=True,
        )
    else:
        server.run(
            transport=transport,
            host=settings.mcp_host,
            port=settings.mcp_port,
        )


if __name__ == "__main__":
    main()
