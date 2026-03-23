"""E2E tests for webhooks — creates, updates, deletes."""

import uuid

import pytest
import httpx

from watermelon_mcp.client import WatermelonClient


@pytest.mark.asyncio
async def test_webhook_lifecycle(client: WatermelonClient) -> None:
    """Create → update → delete a webhook."""
    tag = uuid.uuid4().hex[:8]
    test_url = f"https://e2e-test.example.com/hook-{tag}"

    # Create — returns {"id": int} or just int
    result = await client.post("/webhooks", {
        "url": test_url,
        "action_id": 1,
        "entity_id": 1,
        "verb_id": 1,
    })
    webhook_id = result["id"] if isinstance(result, dict) else result
    assert isinstance(webhook_id, int), f"Expected int ID, got: {result}"

    try:
        # Update — must include all required fields (PUT = full replace)
        updated_url = f"https://e2e-test.example.com/hook-{tag}-updated"
        update_result = await client.put(f"/webhooks/{webhook_id}", {
            "url": updated_url,
            "action_id": 1,
            "entity_id": 1,
            "verb_id": 1,
        })
        # May return 204 or the updated object
        assert update_result is None or isinstance(update_result, (dict, int))

    finally:
        # Cleanup — delete
        delete_result = await client.delete(f"/webhooks/{webhook_id}")
        assert delete_result is None  # 204 No Content


@pytest.mark.asyncio
async def test_webhook_create_requires_all_fields(client: WatermelonClient) -> None:
    """Creating a webhook without required fields returns 422."""
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await client.post("/webhooks", {"url": "https://example.com/hook"})
    assert exc_info.value.response.status_code == 422


@pytest.mark.asyncio
async def test_webhook_get_not_supported(client: WatermelonClient) -> None:
    """GET on a webhook ID returns 405 — API doesn't support listing."""
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await client.get("/webhooks")
    assert exc_info.value.response.status_code == 405
