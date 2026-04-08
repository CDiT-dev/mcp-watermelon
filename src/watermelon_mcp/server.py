"""Watermelon MCP Server entry point."""

import os

from fastmcp import FastMCP
from mcp.types import Icon

from .auth import BearerTokenVerifier
from .client import WatermelonClient
from .settings import get_settings
from .tools_contacts import register_contact_tools
from .tools_conversations import register_conversation_tools
from .tools_messages import register_message_tools
from .tools_fields import register_field_tools
from .tools_webhooks import register_webhook_tools


def create_server() -> FastMCP:
    """Create and configure the FastMCP server with all tools."""
    settings = get_settings()
    client = WatermelonClient(settings.watermelon_api_key, settings.watermelon_secret_key)

    # Bearer token auth (optional — only active when MCP_API_KEY is set)
    _api_key = os.getenv("MCP_API_KEY", "")
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

    return mcp


def main() -> None:
    """Main entry point — run the server with configured transport."""
    settings = get_settings()
    server = create_server()
    server.run(
        transport=settings.mcp_transport,
        host=settings.mcp_host,
        port=settings.mcp_port,
    )


if __name__ == "__main__":
    main()
