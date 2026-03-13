import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod/v4";
import { WatermelonClient } from "../client.js";

export function registerConversationTools(
  server: McpServer,
  client: WatermelonClient,
) {
  server.tool(
    "watermelon_conversations_list",
    "Retrieve all conversations",
    {},
    async () => {
      try {
        const result = await client.get("/conversations");
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );

  server.tool(
    "watermelon_conversations_get",
    "Retrieve a specific conversation with its messages",
    { id: z.string().describe("Conversation ID") },
    async ({ id }) => {
      try {
        const result = await client.get(`/conversations/${encodeURIComponent(id)}`);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );
}
