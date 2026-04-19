"""Conversation tools for Watermelon MCP server."""

import json
from typing import Annotated, Optional
from urllib.parse import quote

from fastmcp import FastMCP
from pydantic import Field

from .client import WatermelonClient


def register_conversation_tools(mcp: FastMCP, client: WatermelonClient) -> None:
    """Register all conversation-related tools."""

    @mcp.tool(name="conversations_list")
    async def conversations_list(
        limit: Annotated[int, Field(ge=1, le=100, description="Number of conversations to return")] = 25,
        page: Annotated[int, Field(ge=0, description="Page number for pagination (0-based)")] = 0,
        date_from: Annotated[Optional[str], "Start of date range filter (ISO 8601, e.g. '2026-01-01T00:00:00Z')"] = None,
        date_to: Annotated[Optional[str], "End of date range filter (ISO 8601)"] = None,
    ) -> str:
        """[crm] List all company conversations with pagination and optional date filtering.

        Returns conversation objects including id, caller_id, user_id, service
        (telegram/facebook/mail/webchat/twitter/whatsapp), is_closed, archived,
        team_id, and a nested messages array.

        Use date_from/date_to to narrow results to a time window.
        Use conversations_get for full details on a single conversation.
        """
        params = f"limit={limit}&page={page}"
        if date_from is not None:
            params += f"&from={quote(date_from, safe='')}"
        if date_to is not None:
            params += f"&to={quote(date_to, safe='')}"
        result = await client.get(f"/all/conversations?{params}")
        return json.dumps(result, indent=2)

    @mcp.tool(name="conversations_get")
    async def conversations_get(
        id: Annotated[str, "Conversation ID (from conversations_list)"],
    ) -> str:
        """[crm] Retrieve a specific conversation including its full message history.

        Returns conversation metadata (id, service, is_closed, team_id, etc.)
        plus all messages with sender, type, payload, and timestamps.

        To reply, pass the conversation id to messages_send.
        """
        result = await client.get(f"/conversations/{quote(id, safe='')}")
        return json.dumps(result, indent=2)
