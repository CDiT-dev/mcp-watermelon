"""Webhook tools for Watermelon MCP server."""

import json
from typing import Annotated, Optional
from urllib.parse import quote

from fastmcp import FastMCP

from .client import WatermelonClient


def register_webhook_tools(mcp: FastMCP, client: WatermelonClient) -> None:
    """Register all webhook-related tools."""

    @mcp.tool(name="watermelon_webhooks_create")
    async def webhooks_create(
        url: Annotated[str, "Webhook callback URL that will receive event notifications"],
        event: Annotated[str, "Event type to subscribe to (e.g., 'conversation.created', 'message.created')"],
    ) -> str:
        """Create a new webhook for event notifications."""
        data = {"url": url, "event": event}
        result = await client.post("/webhooks", data)
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_webhooks_update")
    async def webhooks_update(
        id: Annotated[str, "Webhook ID to update"],
        url: Annotated[Optional[str], "Updated callback URL"] = None,
        event: Annotated[Optional[str], "Updated event type"] = None,
    ) -> str:
        """Update an existing webhook configuration."""
        data = {}
        if url is not None:
            data["url"] = url
        if event is not None:
            data["event"] = event
        if not data:
            return json.dumps({"error": "At least one field (url or event) must be provided"}, indent=2)
        result = await client.put(f"/webhooks/{quote(id, safe='')}", data)
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_webhooks_delete")
    async def webhooks_delete(id: Annotated[str, "Webhook ID to delete"]) -> str:
        """Delete a webhook."""
        result = await client.delete(f"/webhooks/{quote(id, safe='')}")
        if result is None:
            return "Webhook deleted successfully"
        return json.dumps(result, indent=2)
