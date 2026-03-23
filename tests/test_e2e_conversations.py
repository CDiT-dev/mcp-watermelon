"""E2E tests for conversations — uses the correct /all/conversations path."""

import pytest
import httpx

from watermelon_mcp.client import WatermelonClient


@pytest.mark.asyncio
async def test_conversations_list(client: WatermelonClient) -> None:
    """List conversations returns a list, or None/204 if no conversations exist."""
    result = await client.get("/all/conversations?limit=5&page=0")
    # API returns 204 (None) when no conversations exist, or a list
    assert result is None or isinstance(result, (list, dict))


@pytest.mark.asyncio
async def test_conversations_list_with_date_filter(client: WatermelonClient) -> None:
    """List conversations with date range filter doesn't error."""
    result = await client.get(
        "/all/conversations?limit=5&page=0&from=2026-01-01T00:00:00Z&to=2026-12-31T23:59:59Z"
    )
    assert result is None or isinstance(result, (list, dict))


@pytest.mark.asyncio
async def test_conversations_get_first(client: WatermelonClient) -> None:
    """Get the first conversation if any exist."""
    listing = await client.get("/all/conversations?limit=1&page=0")

    if isinstance(listing, list) and listing:
        conv_id = listing[0].get("id")
        if conv_id:
            detail = await client.get(f"/conversations/{conv_id}")
            assert detail is not None
            return

    pytest.skip("No conversations in this Watermelon account")
