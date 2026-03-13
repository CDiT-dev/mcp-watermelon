# 🍉 mcp-watermelon

MCP server for the [Watermelon.ai](https://watermelon.ai) customer support platform. Exposes all 13 public API endpoints as MCP tools, enabling AI assistants to manage contacts, conversations, messages, custom fields, and webhooks.

> 🍉🍉🍉 **DISCLAIMER** 🍉🍉🍉
>
> **This is an unofficial, community-built project.** It is **not** endorsed, supported, or affiliated with [Watermelon.ai](https://watermelon.ai) — *yet*. We built this because we love what they're building and believe MCP integration makes their platform even more powerful. If you're from Watermelon and reading this: let's talk! 🍉

## 🍉 Installation

```bash
npm install -g mcp-watermelon
```

Or clone and build locally:

```bash
git clone https://github.com/cdit-dev/mcp-watermelon.git
cd mcp-watermelon
npm install
npm run build
```

## 🍉 Configuration

Set your Watermelon API credentials as environment variables:

```bash
export WATERMELON_API_KEY="your-api-key"
export WATERMELON_SECRET_KEY="your-secret-key"
```

Get your API credentials from the [Watermelon dashboard](https://watermelon.ai) under Settings → API.

### Claude Desktop / Claude Code

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "watermelon": {
      "command": "npx",
      "args": ["mcp-watermelon"],
      "env": {
        "WATERMELON_API_KEY": "your-api-key",
        "WATERMELON_SECRET_KEY": "your-secret-key"
      }
    }
  }
}
```

## 🍉 Available Tools

### 🍉 Contacts (5 tools)
| Tool | Description |
|------|-------------|
| `watermelon_contacts_create` | Create a new contact with custom fields |
| `watermelon_contacts_get` | Get a specific contact by ID |
| `watermelon_contacts_list` | List all contacts |
| `watermelon_contacts_update` | Update a contact's fields |
| `watermelon_contacts_search` | Search contacts by query |

### 🍉 Conversations (2 tools)
| Tool | Description |
|------|-------------|
| `watermelon_conversations_list` | List all conversations |
| `watermelon_conversations_get` | Get a conversation with messages |

### 🍉 Messages (2 tools)
| Tool | Description |
|------|-------------|
| `watermelon_messages_send` | Send a message |
| `watermelon_messages_get` | Get a specific message |

### 🍉 Custom Fields (1 tool)
| Tool | Description |
|------|-------------|
| `watermelon_fields_list` | List all custom field definitions |

### 🍉 Webhooks (3 tools)
| Tool | Description |
|------|-------------|
| `watermelon_webhooks_create` | Create a webhook |
| `watermelon_webhooks_update` | Update a webhook |
| `watermelon_webhooks_delete` | Delete a webhook |

## 🍉 Use Cases

### For Any Watermelon User

🍉 **Conversational customer support monitoring**
> "Show me all open conversations" → "Summarize the last 5 messages in conversation X" → "Send a follow-up message"

🍉 **Contact management via natural language**
> "Create a contact for Jane Doe, email jane@example.com, company Acme Corp" → "Search for contacts at Acme" → "Update Jane's phone number"

🍉 **Webhook automation setup**
> "Set up a webhook to notify me when new conversations come in" → "Update the webhook URL to point to my new endpoint"

### For Agencies & Platform Builders

🍉 **Contact sync with your CRM**
Use n8n or Zapier to keep contacts in sync between Watermelon and your CRM. When a new contact appears in Watermelon (via webhook), create/update it in your CRM. When a CRM contact is tagged as "support-active", push it to Watermelon with custom fields.

🍉 **AI-first support inbox**
Watermelon's AI chatbot handles first-line conversations. The MCP server lets Claude monitor conversation quality, flag escalations, and send human-assisted responses — all from the same interface you use for everything else.

🍉 **Customer conversation intelligence**
Pull all conversations, analyze sentiment and topics with Claude, generate weekly support digests. Turn your support inbox into actionable business intelligence.

🍉 **Multi-client webhook orchestration**
For each client workspace, set up Watermelon webhooks that feed into your automation platform. New conversation → Slack notification. Conversation resolved → update CRM deal. Message received → log to client timeline.

🍉 **Support-driven content ideas**
Pull customer conversations, use Claude to identify recurring questions and pain points, then turn those into FAQ articles, blog posts, or video content.

### 🍉 With Future API Extensions

These use cases become possible if Watermelon expands the public API (see [GAP_ANALYSIS.md](./GAP_ANALYSIS.md)):

| Use Case | Required API Extension |
|----------|----------------------|
| Auto-close resolved conversations | Conversation lifecycle endpoints |
| AI-assisted knowledge base management | Knowledge base CRUD |
| Support quality dashboard | Analytics read access |
| Dynamic chatbot prompt tuning | Chatbot configuration endpoints |
| Auto-assign conversations by topic | Conversation assignment endpoints |

## 🍉 API Coverage

This server covers **100% of the Watermelon public API** (13 endpoints). See [GAP_ANALYSIS.md](./GAP_ANALYSIS.md) for a detailed analysis of what platform features are and aren't accessible via the API.

## 🍉 About Watermelon

[Watermelon.ai](https://watermelon.ai) is an AI-powered customer support platform that helps businesses automate conversations across channels. They offer a [partner/affiliate program](https://watermelon.ai/partner/) with 25% first-year commission if you want to refer clients.

## 🍉 License

MIT

---

*Built with 🍉 by [CDIT](https://cdit.works)*
