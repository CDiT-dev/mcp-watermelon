## Context

The mcp-watermelon server currently runs as a TypeScript/Node.js project using the raw `@modelcontextprotocol/sdk`. It exposes 13 tools across 5 modules (contacts, conversations, messages, fields, webhooks) that wrap the Watermelon.ai public API at `https://public.watermelon.ai`.

Our standard MCP stack is Python 3.12+ with FastMCP 3.x and `uv` for project/dependency management, as established in mcp-things. That project demonstrates the pattern: `pyproject.toml` with hatchling, `uv` for venv/deps/lockfile, modular tool files, `httpx` for HTTP, `pydantic-settings` for config.

## Goals / Non-Goals

**Goals:**
- 1:1 feature parity — all 13 tools with identical names and parameters
- Follow mcp-things project structure and conventions
- Use FastMCP 3.x decorators for tool registration
- Use `httpx` async client for API calls
- Use `pydantic-settings` for environment variable configuration
- Use `uv` for dependency management and lockfile (`uv.lock`)
- Support stdio transport (primary use case for Claude Desktop)

**Non-Goals:**
- Adding new tools or API coverage beyond current 13
- Streamable-HTTP transport or dashboard (mcp-things has this, but overkill for this PoC)
- Authentication/OAuth (not needed for stdio-only usage)
- Test suite (can be added later)

## Decisions

### 1. Project structure mirrors mcp-things
```
src/watermelon_mcp/
├── __init__.py
├── server.py          # FastMCP server creation + tool registration
├── client.py          # httpx-based WatermelonClient
├── settings.py        # pydantic-settings for env vars
├── tools_contacts.py  # Contact tools (5)
├── tools_conversations.py  # Conversation tools (2)
├── tools_messages.py  # Message tools (2)
├── tools_fields.py    # Field tools (1)
└── tools_webhooks.py  # Webhook tools (3)
```
**Rationale**: Consistent with mcp-things. One tool file per domain keeps things navigable. `server.py` is the entry point that creates the FastMCP instance and registers tools from each module.

### 2. httpx over requests/aiohttp
**Rationale**: Same as mcp-things. httpx is async-native, supports both sync and async, and has a clean API. Already a transitive dependency of FastMCP.

The client MUST be configured with `timeout=30.0` and `follow_redirects=False`. An unexpected redirect could leak the `Authorization` header to a different host.

### 3. pydantic-settings for configuration
Environment variables: `WATERMELON_API_KEY` and `WATERMELON_SECRET_KEY` (unchanged from current).
**Rationale**: Type-safe, validation on startup, consistent with mcp-things pattern.

### 4. Stdio transport only
**Rationale**: This is a PoC server for Claude Desktop integration. Streamable-HTTP can be added later if needed. Keeps the initial migration simple.

### 5. Tool naming preserved
All tool names remain `watermelon_*` (e.g., `watermelon_contacts_create`). Parameter names and types stay identical.
**Rationale**: Zero disruption for existing MCP client configurations.

### 6. Security hardening (from audit)
- **Sanitized error responses**: The httpx client logs full API error details to stderr but returns only the status code to MCP tool responses. Raw Watermelon API error bodies may contain PII and MUST NOT flow back to the LLM.
- **Pagination defaults**: List tools (`watermelon_contacts_list`, `watermelon_conversations_list`) add optional `limit` (default 50, max 100) and `offset` (default 0) parameters to avoid dumping unbounded PII into LLM context.
- **Build scope**: `pyproject.toml` MUST use `tool.hatch.build.targets.wheel.packages` to restrict published artifacts to `src/watermelon_mcp` only — no openspec, `.claude/`, or internal docs.

## Risks / Trade-offs

- **[Breaking change for anyone running the Node version]** → This is a PoC with no known external users. The README will document the new setup.
- **[No tests in initial migration]** → Acceptable for PoC scope. Tool functions are thin wrappers around API calls, easy to test later.
- **[Python 3.12+ requirement]** → Standard for our projects, and FastMCP 3.x requires it anyway.
- **[uv required]** → `uv` is our standard Python project tool. Developers need it installed (`brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`).
