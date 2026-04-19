"""E2E tests for custom fields — read-only, safe to run anytime."""

import json

import pytest

from mcp_watermelon.client import WatermelonClient


@pytest.mark.asyncio
async def test_fields_list(client: WatermelonClient) -> None:
    """fields endpoint returns a list (possibly empty)."""
    result = await client.get("/fields")
    assert isinstance(result, list)
