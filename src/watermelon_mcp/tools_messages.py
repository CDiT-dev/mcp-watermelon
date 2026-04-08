"""Message tools for Watermelon MCP server."""

import json
from typing import Annotated, Literal
from urllib.parse import quote

from fastmcp import FastMCP
from pydantic import Field

from .client import WatermelonClient

_MAX_MESSAGE_LENGTH = 4000

MessageType = Literal[
    "text", "sticker", "photo", "video", "file",
    "activity", "typing", "attachment", "emoji", "location", "contact",
]


def register_message_tools(mcp: FastMCP, client: WatermelonClient) -> None:
    """Register all message-related tools."""

    @mcp.tool(name="messages_send")
    async def messages_send(
        conversation_id: Annotated[int, "Conversation ID to send the message in"],
        user_id: Annotated[int, "User/agent ID sending the message"],
        payload: Annotated[
            str,
            Field(
                min_length=1,
                max_length=_MAX_MESSAGE_LENGTH,
                description=f"Message content (max {_MAX_MESSAGE_LENGTH} characters)",
            ),
        ],
        type: Annotated[
            MessageType,
            "Message type. Use 'text' for normal messages.",
        ] = "text",
    ) -> str:
        """[crm] Send a message in an existing conversation.

        Disambiguation: For live-chat/CRM messages → watermelon. For social media DMs/inbox → zernio.

        All fields are required by the API. conversation_id and user_id are
        integers. The type field defaults to 'text' but supports: text, sticker,
        photo, video, file, activity, typing, attachment, emoji, location, contact.

        Returns the new message's ID on success.
        """
        data = {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "type": type,
            "payload": payload,
        }
        result = await client.post("/messages", data)
        if isinstance(result, int):
            return json.dumps({"id": result}, indent=2)
        return json.dumps(result, indent=2)

    @mcp.tool(name="messages_get")
    async def messages_get(
        id: Annotated[str, "Message ID (from a conversation's message list)"],
    ) -> str:
        """[crm] Retrieve a single message by ID.

        Returns message details: id, conversation_id, user_id, type, payload,
        read status, and timestamps. Returns 204 if not found.

        In most cases, conversations_get already returns all messages
        inline — prefer that over fetching individual messages.
        """
        result = await client.get(f"/messages/{quote(id, safe='')}")
        if isinstance(result, list) and len(result) == 1:
            return json.dumps(result[0], indent=2)
        return json.dumps(result, indent=2)
