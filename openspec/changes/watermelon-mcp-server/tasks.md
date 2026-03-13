## 1. Project Setup

- [x] 1.1 Initialize npm project with `package.json` (name: `mcp-watermelon`, type: module, bin entry)
- [x] 1.2 Configure TypeScript (`tsconfig.json` — target ES2022, module NodeNext, strict)
- [x] 1.3 Install dependencies: `@modelcontextprotocol/sdk`, `zod`
- [x] 1.4 Create project directory structure (`src/`, `src/tools/`)

## 2. Server Core

- [x] 2.1 Implement Watermelon HTTP client (`src/client.ts`) — auth from env vars, base URL, Bearer token construction, error handling for 4xx/5xx/network failures
- [x] 2.2 Implement MCP server entry point (`src/index.ts`) — McpServer init, StdioServerTransport, env var validation, graceful error on missing credentials

## 3. Contact Tools

- [x] 3.1 Implement `watermelon_contacts_create` tool (`src/tools/contacts.ts`)
- [x] 3.2 Implement `watermelon_contacts_get` tool
- [x] 3.3 Implement `watermelon_contacts_list` tool
- [x] 3.4 Implement `watermelon_contacts_update` tool
- [x] 3.5 Implement `watermelon_contacts_search` tool

## 4. Conversation Tools

- [x] 4.1 Implement `watermelon_conversations_list` tool (`src/tools/conversations.ts`)
- [x] 4.2 Implement `watermelon_conversations_get` tool

## 5. Message Tools

- [x] 5.1 Implement `watermelon_messages_send` tool (`src/tools/messages.ts`)
- [x] 5.2 Implement `watermelon_messages_get` tool

## 6. Fields Tool

- [x] 6.1 Implement `watermelon_fields_list` tool (`src/tools/fields.ts`)

## 7. Webhook Tools

- [x] 7.1 Implement `watermelon_webhooks_create` tool (`src/tools/webhooks.ts`)
- [x] 7.2 Implement `watermelon_webhooks_update` tool
- [x] 7.3 Implement `watermelon_webhooks_delete` tool

## 8. Documentation & Packaging

- [x] 8.1 Create `GAP_ANALYSIS.md` — document all 13 endpoints, identify missing platform features, recommendations
- [x] 8.2 Create `README.md` — installation, configuration (env vars), usage with Claude/other MCP clients
- [x] 8.3 Add npm build script and shebang for `bin` entry point
