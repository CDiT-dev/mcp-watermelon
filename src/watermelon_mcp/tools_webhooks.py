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
        url: Annotated[str, "HTTPS callback URL that will receive POST requests when the event fires"],
        action_id: Annotated[int, "Action ID defining the trigger type"],
        entity_id: Annotated[int, "Entity ID defining what object the webhook monitors"],
        verb_id: Annotated[int, "Verb ID defining what operation triggers the webhook"],
    ) -> str:
        """Create a new webhook subscription.

        Watermelon will POST a JSON payload to `url` when the specified
        action/entity/verb combination occurs. Returns the new webhook's
        integer ID on success.

        The action_id, entity_id, and verb_id together define the event.
        Note: the Watermelon API does not support listing webhooks via GET.
        """
        data = {
            "url": url,
            "action_id": action_id,
            "entity_id": entity_id,
            "verb_id": verb_id,
        }
        result = await client.post("/webhooks", data)
        if isinstance(result, int):
            return json.dumps({"id": result}, indent=2)
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_webhooks_update")
    async def webhooks_update(
        id: Annotated[str, "Webhook ID to update"],
        url: Annotated[Optional[str], "Updated HTTPS callback URL"] = None,
        action_id: Annotated[Optional[int], "Updated action ID"] = None,
        entity_id: Annotated[Optional[int], "Updated entity ID"] = None,
        verb_id: Annotated[Optional[int], "Updated verb ID"] = None,
    ) -> str:
        """Update an existing webhook's configuration.

        At least one field must be provided.
        """
        data: dict = {}
        if url is not None:
            data["url"] = url
        if action_id is not None:
            data["action_id"] = action_id
        if entity_id is not None:
            data["entity_id"] = entity_id
        if verb_id is not None:
            data["verb_id"] = verb_id
        if not data:
            return json.dumps({"error": "At least one field must be provided"}, indent=2)
        result = await client.put(f"/webhooks/{quote(id, safe='')}", data)
        if result is None:
            return json.dumps({"status": "updated", "id": id})
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_webhooks_delete")
    async def webhooks_delete(
        id: Annotated[str, "Webhook ID to delete"],
    ) -> str:
        """Delete a webhook and stop receiving its event notifications.

        This action is permanent. Returns confirmation on success.
        """
        result = await client.delete(f"/webhooks/{quote(id, safe='')}")
        if result is None:
            return json.dumps({"status": "deleted", "id": id})
        return json.dumps(result, indent=2)
