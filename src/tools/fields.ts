import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { WatermelonClient } from "../client.js";

export function registerFieldTools(
  server: McpServer,
  client: WatermelonClient,
) {
  server.tool(
    "watermelon_fields_list",
    "Retrieve all custom field definitions",
    {},
    async () => {
      try {
        const result = await client.get("/fields");
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );
}
