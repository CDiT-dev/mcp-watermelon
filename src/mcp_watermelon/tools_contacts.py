"""Contact tools for Watermelon MCP server."""

import json
from typing import Annotated, Any, Optional
from urllib.parse import quote

from fastmcp import FastMCP
from pydantic import Field

from .client import WatermelonClient


def register_contact_tools(mcp: FastMCP, client: WatermelonClient) -> None:
    """Register all contact-related tools."""

    @mcp.tool(name="contacts_create")
    async def contacts_create(
        email_address: Annotated[str, "Email address (must be unique across contacts)"],
        first_name: Annotated[Optional[str], "First name"] = None,
        last_name: Annotated[Optional[str], "Last name"] = None,
        telephone_number: Annotated[Optional[str], "Phone number in any format, e.g. '+49-555-0100'"] = None,
    ) -> str:
        """[crm] Create a new contact in Watermelon.

        Disambiguation: For CRM/live-chat contacts → watermelon. For accounting/invoice contacts → lexoffice.

        email_address is required and must be unique. Returns the new contact's
        ID on success. Contact deletion is not supported by the API — contacts
        can only be created and updated.
        """
        data: dict[str, Any] = {"email_address": email_address}
        if first_name is not None:
            data["first_name"] = first_name
        if last_name is not None:
            data["last_name"] = last_name
        if telephone_number is not None:
            data["telephone_number"] = telephone_number
        result = await client.post("/contacts", data)
        if isinstance(result, int):
            return json.dumps({"id": result}, indent=2)
        return json.dumps(result, indent=2)

    @mcp.tool(name="contacts_get")
    async def contacts_get(id: Annotated[str, "Contact ID (from contacts_list or contacts_search)"]) -> str:
        """[crm] Retrieve a specific contact by ID.

        Returns full contact details including first_name, last_name,
        email_address, telephone_number, status (online/offline), avatar,
        integration source flags, and custom fields.
        """
        result = await client.get(f"/contacts/{quote(id, safe='')}")
        if isinstance(result, list) and len(result) == 1:
            return json.dumps(result[0], indent=2)
        return json.dumps(result, indent=2)

    @mcp.tool(name="contacts_list")
    async def contacts_list(
        limit: Annotated[int, Field(ge=1, le=100, description="Number of contacts to return")] = 25,
        page: Annotated[int, Field(ge=0, description="Page number (0-based)")] = 0,
        without_anonymous: Annotated[bool, "Exclude anonymous contacts from results"] = False,
        date_from: Annotated[Optional[str], "Start of date range filter (ISO 8601)"] = None,
        date_to: Annotated[Optional[str], "End of date range filter (ISO 8601)"] = None,
    ) -> str:
        """[crm] Retrieve contacts with pagination and optional date/anonymity filters.

        Returns an array of contact objects with id, first_name, last_name,
        email_address, telephone_number, status, and custom fields.
        """
        params = f"limit={limit}&page={page}"
        if without_anonymous:
            params += "&withoutAnonymous=true"
        if date_from is not None:
            params += f"&from={quote(date_from, safe='')}"
        if date_to is not None:
            params += f"&to={quote(date_to, safe='')}"
        result = await client.get(f"/contacts?{params}")
        return json.dumps(result, indent=2)

    @mcp.tool(name="contacts_update")
    async def contacts_update(
        id: Annotated[str, "Contact ID to update"],
        first_name: Annotated[Optional[str], "Updated first name"] = None,
        last_name: Annotated[Optional[str], "Updated last name"] = None,
        email_address: Annotated[Optional[str], "Updated email address"] = None,
        telephone_number: Annotated[Optional[str], "Updated phone number"] = None,
    ) -> str:
        """[crm] Update an existing contact. Only provided fields are changed.

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
        if not data:
            return json.dumps({"error": "At least one field must be provided to update"}, indent=2)
        result = await client.put(f"/contacts/{quote(id, safe='')}", data)
        if result is None:
            return json.dumps({"status": "updated", "id": id})
        return json.dumps(result, indent=2)

    @mcp.tool(name="contacts_search")
    async def contacts_search(
        field_value: Annotated[str, "Search query — matches across all contact fields (name, email, phone, etc.)"],
        limit: Annotated[int, Field(ge=1, le=100, description="Maximum results per page")] = 25,
        page: Annotated[int, Field(ge=0, description="Page number (0-based)")] = 0,
    ) -> str:
        """[crm] Search for contacts by field value.

        Disambiguation: For CRM/live-chat contacts → watermelon. For accounting/invoice contacts → lexoffice.

        Searches across all contact fields (name, email, phone, etc.).
        Returns matching contacts with their IDs. Returns 204 if no matches.
        """
        params = f"fieldValue={quote(field_value, safe='')}&limit={limit}&page={page}"
        result = await client.get(f"/contacts/search?{params}")
        return json.dumps(result, indent=2)
