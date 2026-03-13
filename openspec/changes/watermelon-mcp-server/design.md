## Context

Watermelon.ai is a customer support AI platform. Its public REST API at `https://public.watermelon.ai` exposes 13 endpoints covering contacts, conversations, messages, custom fields, and webhooks. Authentication uses Bearer tokens formatted as `api_key.secret_key`. Rate limits: 100 concurrent requests per source, 500 requests per minute.

This is a greenfield TypeScript project building an MCP server that wraps these endpoints as tools, enabling any MCP-compatible AI assistant to manage a Watermelon workspace.

## Goals / Non-Goals

**Goals:**
- Expose all 13 Watermelon API endpoints as MCP tools via stdio transport
- Provide clear tool descriptions and typed input schemas so LLMs can use them effectively
- Handle authentication, errors, and rate limits gracefully
- Ship as an installable npm package (`mcp-watermelon`)
- Document API coverage gaps

**Non-Goals:**
- Building a UI or CLI beyond the MCP server itself
- Implementing webhook receivers (only webhook CRUD management)
- Caching or local state beyond what's needed for a single request
- Supporting SSE or HTTP transport (stdio only for PoC)
- Watermelon internal/private API endpoints

## Decisions

### 1. TypeScript + MCP SDK high-level API
Use `@modelcontextprotocol/sdk` with `McpServer` class and `registerTool`. This gives us typed tool registration with Zod schemas and handles all protocol plumbing.

**Alternative**: Low-level `Server` class — rejected because the high-level API covers our needs and requires less boilerplate.

### 2. Native fetch for HTTP client
Use Node.js built-in `fetch` (Node 18+). No need for axios or node-fetch — keeps dependencies minimal.

**Alternative**: axios — rejected to minimize dependency footprint for a PoC.

### 3. One tool per API endpoint
Each of the 13 endpoints maps to exactly one MCP tool. Tool names follow the pattern `watermelon_{resource}_{action}` (e.g., `watermelon_contacts_create`, `watermelon_conversations_list`).

**Alternative**: Grouped tools (e.g., one "contacts" tool with sub-actions) — rejected because discrete tools are easier for LLMs to discover and use.

### 4. Environment variable authentication
API key and secret key provided via `WATERMELON_API_KEY` and `WATERMELON_SECRET_KEY` environment variables. Concatenated as `${apiKey}.${secretKey}` for the Bearer token.

**Alternative**: Config file — rejected as env vars are the standard for MCP servers and simpler for users.

### 5. Project structure
```
src/
  index.ts          # Server entry point + transport setup
  client.ts         # Watermelon HTTP client (auth, base URL, error handling)
  tools/
    contacts.ts     # 5 tools: create, get, get-all, update, search
    conversations.ts # 2 tools: list, get
    messages.ts     # 2 tools: send, get
    fields.ts       # 1 tool: list
    webhooks.ts     # 3 tools: create, update, delete
```

### 6. Zod v4 for input schemas
MCP SDK uses Zod v4 (`zod/v4`). Each tool defines its input schema using Zod, which the SDK converts to JSON Schema for the MCP protocol.

## Risks / Trade-offs

- **Incomplete API documentation** → The public docs lack detailed request/response schemas. Mitigation: test against a real Watermelon instance and iterate. Document gaps in gap-analysis.
- **Rate limiting** → 500 req/min is generous for interactive use but could be hit by batch operations. Mitigation: return clear error messages on 429 responses; no client-side throttling for PoC.
- **API changes** → No versioned API path visible. Mitigation: pin to current behavior, document in gap analysis.
- **Auth token in env vars** → Standard practice but tokens could leak in logs. Mitigation: never log the token; use `console.error` for all logging (stdout reserved for MCP protocol).
