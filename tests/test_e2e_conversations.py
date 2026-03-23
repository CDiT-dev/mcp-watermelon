"""E2E tests for conversations.

Note: The conversations endpoint returns 503 when no Watermelon chatbot is
configured in the account. These tests gracefully handle that case.
"""

import pytest
import httpx

from watermelon_mcp.client import WatermelonClient


@pytest.mark.asyncio
async def test_conversations_list(client: WatermelonClient) -> None:
    """List conversations — may return 503 if no chatbot is configured."""
    try:
        result = await client.get("/conversations?limit=5&offset=0")
        assert isinstance(result, (list, dict))
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 503:
            pytest.skip("Conversations endpoint returns 503 — no chatbot configured")
        raise


@pytest.mark.asyncio
async def test_conversations_get_first(client: WatermelonClient) -> None:
    """Get the first conversation if any exist."""
    try:
        listing = await client.get("/conversations?limit=1&offset=0")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 503:
            pytest.skip("Conversations endpoint returns 503 — no chatbot configured")
        raise

    if isinstance(listing, list) and listing:
        conv_id = listing[0].get("id")
        if conv_id:
            detail = await client.get(f"/conversations/{conv_id}")
            assert detail is not None
    else:
        pytest.skip("No conversations in this Watermelon account")
