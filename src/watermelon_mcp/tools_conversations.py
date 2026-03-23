"""Conversation tools for Watermelon MCP server."""

import json
from typing import Annotated
from urllib.parse import quote

from fastmcp import FastMCP

from .client import WatermelonClient


def register_conversation_tools(mcp: FastMCP, client: WatermelonClient) -> None:
    """Register all conversation-related tools."""

    @mcp.tool(name="watermelon_conversations_list")
    async def conversations_list(
        limit: Annotated[int, "Number of conversations to return (1-100)"] = 50,
        offset: Annotated[int, "Number of conversations to skip for pagination"] = 0,
    ) -> str:
        """Retrieve conversations with pagination. Defaults to first 50."""
        limit = max(1, min(limit, 100))
        result = await client.get(f"/conversations?limit={limit}&offset={offset}")
        return json.dumps(result, indent=2)

    @mcp.tool(name="watermelon_conversations_get")
    async def conversations_get(id: Annotated[str, "Conversation ID"]) -> str:
        """Retrieve a specific conversation with its messages."""
        result = await client.get(f"/conversations/{quote(id, safe='')}")
        return json.dumps(result, indent=2)
