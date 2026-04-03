## Why

The current MCP server is built in TypeScript with the raw `@modelcontextprotocol/sdk`. Our standard stack for MCP servers is Python + FastMCP 3.x (as used in mcp-things). Migrating now aligns this project with our tooling, makes maintenance easier, and gives us FastMCP's built-in features (tool annotations, typed parameters, transport handling) for free.

## What Changes

- **BREAKING**: Remove entire TypeScript codebase (`src/`, `package.json`, `tsconfig.json`, `node_modules/`)
- **BREAKING**: Replace with Python/FastMCP 3.x server following mcp-things project structure
- New `pyproject.toml` with hatchling build, `uv` for dependency management
- New `src/watermelon_mcp/` Python package with modular tool files
- HTTP client using `httpx` instead of raw `fetch`
- All 13 existing tools preserved with identical MCP tool names and functionality
- Configuration via `pydantic-settings` for environment variables

## Capabilities

### New Capabilities
- `python-server`: FastMCP 3.x server setup, entry point, transport configuration
- `watermelon-client`: httpx-based async HTTP client for Watermelon API
- `contact-tools`: Contact CRUD and search tools (5 tools)
- `conversation-tools`: Conversation list and get tools (2 tools)
- `message-tools`: Message send and get tools (2 tools)
- `field-tools`: Custom field listing tool (1 tool)
- `webhook-tools`: Webhook create, update, delete tools (3 tools)

### Modified Capabilities
_(none — no existing openspec specs)_

## Impact

- **Code**: Complete replacement of `src/` TypeScript with `src/watermelon_mcp/` Python
- **Dependencies**: Node.js/npm → Python 3.12+/uv; `@modelcontextprotocol/sdk` + `zod` → `fastmcp` + `httpx` + `pydantic-settings`
- **Build**: `tsc` → `hatchling`; `package.json` → `pyproject.toml`
- **Config**: Same env vars (`WATERMELON_API_KEY`, `WATERMELON_SECRET_KEY`) but loaded via pydantic-settings
- **MCP clients**: Tool names and parameters remain identical — no client-side changes needed
