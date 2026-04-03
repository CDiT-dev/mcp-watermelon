"""Watermelon MCP Server entry point."""

from fastmcp import FastMCP
from mcp.types import Icon

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

    # Keycloak auth (optional — only active when keycloak_issuer is set)
    auth = None
    if settings.keycloak_issuer:
        from .auth import build_auth

        auth = build_auth(
            keycloak_issuer=settings.keycloak_issuer,
            keycloak_client_id=settings.keycloak_client_id,
            keycloak_client_secret=settings.keycloak_client_secret,
            base_url=settings.mcp_base_url or f"http://{settings.mcp_host}:{settings.mcp_port}",
            api_key=settings.mcp_api_key,
        )

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
