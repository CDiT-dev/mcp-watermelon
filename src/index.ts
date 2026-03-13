#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { WatermelonClient } from "./client.js";
import { registerContactTools } from "./tools/contacts.js";
import { registerConversationTools } from "./tools/conversations.js";
import { registerMessageTools } from "./tools/messages.js";
import { registerFieldTools } from "./tools/fields.js";
import { registerWebhookTools } from "./tools/webhooks.js";

const apiKey = process.env.WATERMELON_API_KEY;
const secretKey = process.env.WATERMELON_SECRET_KEY;

if (!apiKey) {
  console.error("Error: WATERMELON_API_KEY environment variable is required");
  process.exit(1);
}

if (!secretKey) {
  console.error(
    "Error: WATERMELON_SECRET_KEY environment variable is required",
  );
  process.exit(1);
}

const client = new WatermelonClient({ apiKey, secretKey });

const server = new McpServer({
  name: "mcp-watermelon",
  version: "0.1.0",
});

registerContactTools(server, client);
registerConversationTools(server, client);
registerMessageTools(server, client);
registerFieldTools(server, client);
registerWebhookTools(server, client);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("mcp-watermelon server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
