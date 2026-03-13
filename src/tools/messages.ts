import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod/v4";
import { WatermelonClient } from "../client.js";

export function registerMessageTools(
  server: McpServer,
  client: WatermelonClient,
) {
  server.tool(
    "watermelon_messages_send",
    "Send a new message in a conversation",
    { data: z.record(z.string(), z.unknown()).describe("Message data (text content, conversation/contact target)") },
    async ({ data }) => {
      try {
        const result = await client.post("/messages", data);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );

  server.tool(
    "watermelon_messages_get",
    "Retrieve a specific message by ID",
    { id: z.string().describe("Message ID") },
    async ({ id }) => {
      try {
        const result = await client.get(`/messages/${encodeURIComponent(id)}`);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );
}
