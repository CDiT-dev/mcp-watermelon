"""Message tools for Watermelon MCP server."""

import json
from typing import Annotated, Any, Optional
from urllib.parse import quote

from fastmcp import FastMCP
from pydantic import Field

from .client import WatermelonClient

_MAX_MESSAGE_LENGTH = 4000


def register_message_tools(mcp: FastMCP, client: WatermelonClient) -> None:
    """Register all message-related tools."""

    @mcp.tool(name="watermelon_messages_send")
    async def messages_send(
        conversation_id: Annotated[
            str,
            "Conversation ID to send the message in (from watermelon_conversations_list)",
        ],
        payload: Annotated[
            str,
            Field(
                min_length=1,
                max_length=_MAX_MESSAGE_LENGTH,
                description=f"Message text content (max {_MAX_MESSAGE_LENGTH} characters)",
            ),
        ],
        user_id: Annotated[
            Optional[str],
            "User/agent ID sending the message. Required by the API.",
        ] = None,
    ) -> str:
        """Send a text message in an existing conversation.

        The message appears in the conversation thread. The API requires
        user_id to identify the sender. The payload field contains the
        message text (max 4000 characters).
        """
        data: dict[str, Any] = {
            "conversation_id": conversation_id,
            "payload": payload,
            "type": "text",
        }
        if user_id is not None:
            data["user_id"] = user_id
        result = await client.post("/messages", data)
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_messages_get")
    async def messages_get(
        id: Annotated[
            str,
            "Message ID (from a conversation's message list)",
        ],
    ) -> str:
        """Retrieve a single message by ID.

        Returns message details including conversation_id, payload, type,
        user_id, and timestamps. The API returns an array — this tool
        returns the first match.

        In most cases, watermelon_conversations_get already returns all
        messages for a conversation — prefer that over calling this per message.
        """
        result = await client.get(f"/messages/{quote(id, safe='')}")
        if isinstance(result, list) and len(result) == 1:
            return json.dumps(result[0], indent=2)
        return json.dumps(result, indent=2)
