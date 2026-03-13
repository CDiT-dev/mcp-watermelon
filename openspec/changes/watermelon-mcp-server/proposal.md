## Why

Watermelon.ai is a customer support AI platform with a public REST API (13 endpoints) covering contacts, conversations, messages, custom fields, and webhooks. There is no MCP server for it, meaning AI assistants cannot natively interact with Watermelon workspaces. Building an open-source MCP server unlocks this — and the CEO is family (brother-in-law), making this a strategic play: working product → CEO conversation → technology partnership + consulting engagement.

## What Changes

- New TypeScript MCP server package exposing all 13 Watermelon public API endpoints as MCP tools
- Bearer token authentication (API key + secret key concatenated with `.`)
- Proper error handling mapping Watermelon HTTP status codes to MCP error responses
- Rate limit awareness (100 concurrent / 500 per minute)
- Gap analysis documentation showing what is and isn't reachable via the public API
- Published as open-source npm package

## Capabilities

### New Capabilities
- `contacts-tools`: MCP tools for contact CRUD — create, get, get-all, update, search contacts with custom fields
- `conversations-tools`: MCP tools for conversation retrieval — list all conversations, get specific conversation with messages
- `messages-tools`: MCP tools for messaging — send messages, retrieve specific messages
- `fields-tools`: MCP tool for retrieving custom field definitions
- `webhooks-tools`: MCP tools for webhook management — create, update, delete webhooks
- `server-core`: MCP server setup, authentication, HTTP client, error handling, and transport configuration
- `gap-analysis`: Documentation of API coverage gaps — what Watermelon features are NOT reachable via the public API

### Modified Capabilities

## Impact

- New npm package: `mcp-watermelon`
- Dependencies: `@modelcontextprotocol/sdk`, `zod`, HTTP client (native fetch or similar)
- External dependency: Watermelon public API at `https://public.watermelon.ai`
- No existing code affected (greenfield project)
