"""Contact tools for Watermelon MCP server."""

import json
from typing import Annotated, Any, Optional
from urllib.parse import quote

from fastmcp import FastMCP
from pydantic import Field

from .client import WatermelonClient


def register_contact_tools(mcp: FastMCP, client: WatermelonClient) -> None:
    """Register all contact-related tools."""

    @mcp.tool(name="watermelon_contacts_create")
    async def contacts_create(
        email_address: Annotated[str, "Email address (required, must be unique)"],
        first_name: Annotated[Optional[str], "First name"] = None,
        last_name: Annotated[Optional[str], "Last name"] = None,
        telephone_number: Annotated[Optional[str], "Phone number in any format, e.g. '+49-555-0100'"] = None,
        location: Annotated[Optional[str], "Location / city"] = None,
    ) -> str:
        """Create a new contact in Watermelon.

        email_address is required and must be unique across all contacts.
        Returns the new contact's integer ID on success.
        """
        data: dict[str, Any] = {"email_address": email_address}
        if first_name is not None:
            data["first_name"] = first_name
        if last_name is not None:
            data["last_name"] = last_name
        if telephone_number is not None:
            data["telephone_number"] = telephone_number
        if location is not None:
            data["location"] = location
        result = await client.post("/contacts", data)
        # API may return {"id": int} or just int
        if isinstance(result, int):
            return json.dumps({"id": result}, indent=2)
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_contacts_get")
    async def contacts_get(id: Annotated[str, "Contact ID (from contacts_list or contacts_search)"]) -> str:
        """Retrieve a specific contact by ID.

        Returns full contact details including first_name, last_name,
        email_address, telephone_number, status, and timestamps.
        The API returns an array — this tool returns the first match.
        """
        result = await client.get(f"/contacts/{quote(id, safe='')}")
        # API returns a list even for single ID lookup
        if isinstance(result, list) and len(result) == 1:
            return json.dumps(result[0], indent=2)
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_contacts_list")
    async def contacts_list(
        limit: Annotated[int, Field(ge=1, le=100, description="Number of contacts to return")] = 50,
        offset: Annotated[int, Field(ge=0, description="Number of contacts to skip for pagination")] = 0,
    ) -> str:
        """Retrieve contacts with pagination. Defaults to first 50.

        Returns an array of contact objects with id, first_name, last_name,
        email_address, telephone_number, status, and timestamps.
        Use offset to page through results.
        """
        result = await client.get(f"/contacts?limit={limit}&offset={offset}")
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_contacts_update")
    async def contacts_update(
        id: Annotated[str, "Contact ID to update"],
        first_name: Annotated[Optional[str], "Updated first name"] = None,
        last_name: Annotated[Optional[str], "Updated last name"] = None,
        email_address: Annotated[Optional[str], "Updated email address"] = None,
        telephone_number: Annotated[Optional[str], "Updated phone number"] = None,
        location: Annotated[Optional[str], "Updated location"] = None,
    ) -> str:
        """Update an existing contact. Only provided fields are changed.

        Returns 204 on success (no body). Contact deletion is not supported
        by the Watermelon API.
        """
        data: dict[str, Any] = {}
        if first_name is not None:
            data["first_name"] = first_name
        if last_name is not None:
            data["last_name"] = last_name
        if email_address is not None:
            data["email_address"] = email_address
        if telephone_number is not None:
            data["telephone_number"] = telephone_number
        if location is not None:
            data["location"] = location
        if not data:
            return json.dumps({"error": "At least one field must be provided to update"}, indent=2)
        result = await client.put(f"/contacts/{quote(id, safe='')}", data)
        if result is None:
            return json.dumps({"status": "updated", "id": id})
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_contacts_search")
    async def contacts_search(
        field_value: Annotated[str, "Value to search for across contact fields"],
        field_id: Annotated[Optional[int], "Restrict search to a specific field ID (from watermelon_fields_list). Omit to search all fields."] = None,
    ) -> str:
        """Search for contacts by field value.

        Searches across contact fields. Use field_id to restrict to a specific
        field (call watermelon_fields_list to discover field IDs).
        Common field IDs: 1=first_name, 2=last_name, 3=email_address, 4=phone_number.

        Returns matching contacts with their IDs.
        """
        params = f"fieldValue={quote(field_value, safe='')}"
        if field_id is not None:
            params += f"&fieldId={field_id}"
        result = await client.get(f"/contacts/search?{params}")
        return json.dumps(result, indent=2)
