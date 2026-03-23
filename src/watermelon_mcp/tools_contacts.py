"""Contact tools for Watermelon MCP server."""

import json
from typing import Annotated, Any, Optional
from urllib.parse import quote

from fastmcp import FastMCP

from .client import WatermelonClient


def register_contact_tools(mcp: FastMCP, client: WatermelonClient) -> None:
    """Register all contact-related tools."""

    @mcp.tool(name="watermelon_contacts_create")
    async def contacts_create(
        name: Annotated[str, "Full name of the contact"],
        email: Annotated[Optional[str], "Email address"] = None,
        phone: Annotated[Optional[str], "Phone number"] = None,
        company: Annotated[Optional[str], "Company name"] = None,
        custom_fields: Annotated[Optional[dict[str, Any]], "Additional custom fields as key-value pairs (use watermelon_fields_list to discover available fields)"] = None,
    ) -> str:
        """Create a new contact in Watermelon.

        Use watermelon_fields_list first to discover available custom fields.
        """
        data: dict[str, Any] = {"name": name}
        if email is not None:
            data["email"] = email
        if phone is not None:
            data["phone"] = phone
        if company is not None:
            data["company"] = company
        if custom_fields:
            data.update(custom_fields)
        result = await client.post("/contacts", data)
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_contacts_get")
    async def contacts_get(id: Annotated[str, "Contact ID"]) -> str:
        """Retrieve a specific contact by ID."""
        result = await client.get(f"/contacts/{quote(id, safe='')}")
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_contacts_list")
    async def contacts_list(
        limit: Annotated[int, "Number of contacts to return (1-100)"] = 50,
        offset: Annotated[int, "Number of contacts to skip for pagination"] = 0,
    ) -> str:
        """Retrieve contacts with pagination. Defaults to first 50."""
        limit = max(1, min(limit, 100))
        result = await client.get(f"/contacts?limit={limit}&offset={offset}")
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_contacts_update")
    async def contacts_update(
        id: Annotated[str, "Contact ID to update"],
        name: Annotated[Optional[str], "Updated full name"] = None,
        email: Annotated[Optional[str], "Updated email address"] = None,
        phone: Annotated[Optional[str], "Updated phone number"] = None,
        company: Annotated[Optional[str], "Updated company name"] = None,
        custom_fields: Annotated[Optional[dict[str, Any]], "Additional custom fields to update as key-value pairs"] = None,
    ) -> str:
        """Update an existing contact's information. Only provided fields are updated."""
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if email is not None:
            data["email"] = email
        if phone is not None:
            data["phone"] = phone
        if company is not None:
            data["company"] = company
        if custom_fields:
            data.update(custom_fields)
        if not data:
            return json.dumps({"error": "At least one field must be provided to update"}, indent=2)
        result = await client.put(f"/contacts/{quote(id, safe='')}", data)
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_contacts_search")
    async def contacts_search(
        query: Annotated[str, "Search query (name, email, phone, or company)"],
    ) -> str:
        """Search for contacts matching a query string."""
        result = await client.get(f"/contacts/search?query={quote(query, safe='')}")
        return json.dumps(result, indent=2)
