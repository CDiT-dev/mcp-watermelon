import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod/v4";
import { WatermelonClient } from "../client.js";

export function registerContactTools(
  server: McpServer,
  client: WatermelonClient,
) {
  server.tool(
    "watermelon_contacts_create",
    "Create a new contact in Watermelon with optional custom fields",
    { data: z.record(z.string(), z.unknown()).describe("Contact data (name, email, custom fields, etc.)") },
    async ({ data }) => {
      try {
        const result = await client.post("/contacts", data);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );

  server.tool(
    "watermelon_contacts_get",
    "Retrieve a specific contact by ID",
    { id: z.string().describe("Contact ID") },
    async ({ id }) => {
      try {
        const result = await client.get(`/contacts/${encodeURIComponent(id)}`);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );

  server.tool(
    "watermelon_contacts_list",
    "Retrieve all contacts and their fields",
    {},
    async () => {
      try {
        const result = await client.get("/contacts");
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );

  server.tool(
    "watermelon_contacts_update",
    "Update an existing contact's information",
    {
      id: z.string().describe("Contact ID"),
      data: z.record(z.string(), z.unknown()).describe("Fields to update"),
    },
    async ({ id, data }) => {
      try {
        const result = await client.put(`/contacts/${encodeURIComponent(id)}`, data);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );

  server.tool(
    "watermelon_contacts_search",
    "Search for contacts matching a query",
    { query: z.string().describe("Search query string") },
    async ({ query }) => {
      try {
        const result = await client.get(`/contacts/search?query=${encodeURIComponent(query)}`);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (e) {
        return { content: [{ type: "text", text: String(e) }], isError: true };
      }
    },
  );
}
