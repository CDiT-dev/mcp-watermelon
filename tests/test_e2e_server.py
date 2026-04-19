"""E2E tests for MCP server creation and tool registration."""

import pytest

from mcp_watermelon.server import create_server


def test_server_creates_successfully() -> None:
    """Server initializes without errors."""
    server = create_server()
    assert server is not None


@pytest.mark.asyncio
async def test_server_has_expected_tools() -> None:
    """Server registers all expected tools."""
    server = create_server()
    tools = await server.list_tools()
    tool_names = {t.name for t in tools}
    expected_names = {
        "watermelon_contacts_create",
        "watermelon_contacts_get",
        "watermelon_contacts_list",
        "watermelon_contacts_update",
        "watermelon_contacts_search",
        "watermelon_conversations_list",
        "watermelon_conversations_get",
        "watermelon_messages_send",
        "watermelon_messages_get",
        "watermelon_fields_list",
        "watermelon_webhooks_create",
        "watermelon_webhooks_update",
        "watermelon_webhooks_delete",
    }
    assert expected_names == tool_names, f"Missing: {expected_names - tool_names}, Extra: {tool_names - expected_names}"


@pytest.mark.asyncio
async def test_tool_schemas_have_descriptions() -> None:
    """Every tool has a non-empty description."""
    server = create_server()
    tools = await server.list_tools()
    for tool in tools:
        assert tool.description, f"Tool {tool.name} has no description"
        assert len(tool.description) > 20, f"Tool {tool.name} has a very short description: {tool.description}"
