import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod/v4";
import { WatermelonClient } from "../client.js";

export function registerWebhookTools(
  server: McpServer,
  client: WatermelonClient,
) {
  server.tool(
    "watermelon_webhooks_create",
    "Create a new webhook for event notifications",
    { data: z.record(z.string(), z.unknown()).describe("Webhook configuration (callback URL, event triggers)") },
    async ({ data }) => {
      try {
        const result = await client.post("/webhooks", data);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );

  server.tool(
    "watermelon_webhooks_update",
    "Update an existing webhook configuration",
    {
      id: z.string().describe("Webhook ID"),
      data: z.record(z.string(), z.unknown()).describe("Updated webhook settings"),
    },
    async ({ id, data }) => {
      try {
        const result = await client.put(`/webhooks/${encodeURIComponent(id)}`, data);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );

  server.tool(
    "watermelon_webhooks_delete",
    "Delete a webhook",
    { id: z.string().describe("Webhook ID") },
    async ({ id }) => {
      try {
        const result = await client.del(`/webhooks/${encodeURIComponent(id)}`);
        return { content: [{ type: "text", text: result ? JSON.stringify(result, null, 2) : "Webhook deleted successfully" }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );
}
