"""Field tools for Watermelon MCP server."""

import json

from fastmcp import FastMCP

from .client import WatermelonClient


def register_field_tools(mcp: FastMCP, client: WatermelonClient) -> None:
    """Register all field-related tools."""

    @mcp.tool(name="watermelon_fields_list")
    async def fields_list() -> str:
        """List all custom field definitions configured in Watermelon.

        Returns each field's key, label, type (e.g. 'text', 'number', 'boolean',
        'select'), and any allowed values for select fields.

        Call this before watermelon_contacts_create or watermelon_contacts_update
        to discover which keys to pass in the custom_fields parameter. For example,
        if this returns a field with key 'plan_tier', you would pass
        custom_fields={"plan_tier": "enterprise"} when creating a contact.
        """
        result = await client.get("/fields")
        return json.dumps(result, indent=2)
