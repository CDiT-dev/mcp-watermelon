"""Message tools for Watermelon MCP server."""

import json
from typing import Annotated
from urllib.parse import quote

from fastmcp import FastMCP

from .client import WatermelonClient


def register_message_tools(mcp: FastMCP, client: WatermelonClient) -> None:
    """Register all message-related tools."""

    @mcp.tool(name="watermelon_messages_send")
    async def messages_send(
        conversation_id: Annotated[str, "ID of the conversation to send the message in"],
        content: Annotated[str, "Message text content"],
    ) -> str:
        """Send a new message in a conversation.

        The message is sent as a text message from the agent/bot.
        """
        data = {
            "conversationId": conversation_id,
            "content": content,
        }
        result = await client.post("/messages", data)
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_messages_get")
    async def messages_get(id: Annotated[str, "Message ID"]) -> str:
        """Retrieve a specific message by ID."""
        result = await client.get(f"/messages/{quote(id, safe='')}")
        return json.dumps(result, indent=2)
