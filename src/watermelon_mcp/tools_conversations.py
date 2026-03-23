"""Conversation tools for Watermelon MCP server."""

import json
from typing import Annotated
from urllib.parse import quote

from fastmcp import FastMCP
from pydantic import Field

from .client import WatermelonClient


def register_conversation_tools(mcp: FastMCP, client: WatermelonClient) -> None:
    """Register all conversation-related tools."""

    @mcp.tool(name="watermelon_conversations_list")
    async def conversations_list(
        limit: Annotated[int, Field(ge=1, le=100, description="Number of conversations to return")] = 50,
        offset: Annotated[int, Field(ge=0, description="Number of conversations to skip for pagination")] = 0,
    ) -> str:
        """List conversations with pagination.

        Returns conversation summaries. Use watermelon_conversations_get to
        fetch full message history for a specific conversation.

        Note: This endpoint requires an active Watermelon chatbot to be
        configured. Returns 503 if no chatbot is set up.
        """
        result = await client.get(f"/conversations?limit={limit}&offset={offset}")
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_conversations_get")
    async def conversations_get(
        id: Annotated[str, "Conversation ID (from watermelon_conversations_list)"],
    ) -> str:
        """Retrieve a specific conversation including its full message history.

        Returns conversation metadata plus all messages in chronological order
        with sender, content, and timestamp.

        To reply, pass the conversation id to watermelon_messages_send.
        """
        result = await client.get(f"/conversations/{quote(id, safe='')}")
        return json.dumps(result, indent=2)
