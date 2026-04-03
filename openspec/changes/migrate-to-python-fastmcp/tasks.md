## 1. Project Setup

- [x] 1.1 Create `pyproject.toml` with hatchling build, dependencies (fastmcp>=3.1.0, httpx>=0.28.1, pydantic-settings>=2.12.0), `server` script entry point, and `tool.hatch.build.targets.wheel.packages` scoped to `src/watermelon_mcp` only
- [x] 1.2 Run `uv sync` to create venv and generate `uv.lock`
- [x] 1.3 Create `src/watermelon_mcp/__init__.py`
- [x] 1.4 Create `src/watermelon_mcp/settings.py` with pydantic-settings config for `WATERMELON_API_KEY` and `WATERMELON_SECRET_KEY`

## 2. HTTP Client

- [x] 2.1 Create `src/watermelon_mcp/client.py` with async `WatermelonClient` using httpx — GET, POST, PUT, DELETE methods with Bearer auth, error handling, 204/429 handling, `timeout=30.0`, `follow_redirects=False`, and sanitized error messages (log full error to stderr, return only status code to caller)

## 3. Tool Modules

- [x] 3.1 Create `src/watermelon_mcp/tools_contacts.py` — 5 tools: create, get, list (with `limit`/`offset` params, default 50), update, search
- [x] 3.2 Create `src/watermelon_mcp/tools_conversations.py` — 2 tools: list (with `limit`/`offset` params, default 50), get
- [x] 3.3 Create `src/watermelon_mcp/tools_messages.py` — 2 tools: send, get
- [x] 3.4 Create `src/watermelon_mcp/tools_fields.py` — 1 tool: list
- [x] 3.5 Create `src/watermelon_mcp/tools_webhooks.py` — 3 tools: create, update, delete

## 4. Server Entry Point

- [x] 4.1 Create `src/watermelon_mcp/server.py` — FastMCP server creation, tool registration from all modules, stdio main function

## 5. Cleanup

- [x] 5.1 Remove TypeScript source files (`src/index.ts`, `src/client.ts`, `src/tools/`)
- [x] 5.2 Remove Node.js config files (`package.json`, `tsconfig.json`, `package-lock.json`)
- [x] 5.3 Update README.md with Python/uv setup instructions (`uv sync`, `uv run server`)
