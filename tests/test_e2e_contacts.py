"""E2E tests for contacts — creates, reads, searches, updates against live API."""

import json
import uuid

import pytest

from watermelon_mcp.client import WatermelonClient


@pytest.fixture
def unique_email() -> str:
    """Generate a unique email so tests don't collide."""
    return f"e2e-{uuid.uuid4().hex[:8]}@cdit-test.example"


@pytest.mark.asyncio
async def test_contacts_list(client: WatermelonClient) -> None:
    """List contacts returns a list."""
    result = await client.get("/contacts?limit=5&offset=0")
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_contact_create_get_search_update(client: WatermelonClient, unique_email: str) -> None:
    """Create → get → search → update a contact (no delete — API doesn't support it)."""
    # Create — returns {"id": <int>} or just an int
    result = await client.post("/contacts", {
        "email_address": unique_email,
        "first_name": "E2E",
        "last_name": "TestContact",
    })
    if isinstance(result, dict):
        contact_id = result["id"]
    else:
        contact_id = result
    assert isinstance(contact_id, int), f"Expected int ID, got: {result}"

    # Get by ID — returns a list with one element
    fetched = await client.get(f"/contacts/{contact_id}")
    assert isinstance(fetched, list)
    assert len(fetched) == 1
    assert fetched[0]["email_address"] == unique_email
    assert fetched[0]["first_name"] == "E2E"

    # Search by field value
    search_result = await client.get(f"/contacts/search?fieldValue={unique_email}")
    assert isinstance(search_result, list)
    assert any(c["id"] == contact_id for c in search_result)

    # Search with fieldId (3 = email_address)
    search_by_field = await client.get(f"/contacts/search?fieldValue={unique_email}&fieldId=3")
    assert isinstance(search_by_field, list)
    assert any(c["id"] == contact_id for c in search_by_field)

    # Update — returns 204 (None)
    update_result = await client.put(f"/contacts/{contact_id}", {
        "last_name": "Updated",
    })
    assert update_result is None  # 204 No Content

    # Verify update
    refetched = await client.get(f"/contacts/{contact_id}")
    assert refetched[0]["last_name"] == "Updated"


@pytest.mark.asyncio
async def test_contact_create_requires_email(client: WatermelonClient) -> None:
    """Creating a contact without email_address returns 422."""
    import httpx

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await client.post("/contacts", {"first_name": "NoEmail"})
    assert exc_info.value.response.status_code == 422
