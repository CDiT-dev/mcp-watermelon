# Watermelon API — Gap Analysis

## Available Endpoints (13 total)

All endpoints use `https://public.watermelon.ai` with Bearer token auth (`api_key.secret_key`).

| # | Method | Path | MCP Tool | What It Does |
|---|--------|------|----------|--------------|
| 1 | POST | `/contacts` | `watermelon_contacts_create` | Create a contact with custom fields |
| 2 | GET | `/contacts` | `watermelon_contacts_list` | List all contacts |
| 3 | GET | `/contacts/{id}` | `watermelon_contacts_get` | Get a specific contact |
| 4 | PUT | `/contacts/{id}` | `watermelon_contacts_update` | Update a contact |
| 5 | GET | `/contacts/search` | `watermelon_contacts_search` | Search contacts |
| 6 | GET | `/conversations` | `watermelon_conversations_list` | List all conversations |
| 7 | GET | `/conversations/{id}` | `watermelon_conversations_get` | Get a conversation with messages |
| 8 | POST | `/messages` | `watermelon_messages_send` | Send a message |
| 9 | GET | `/messages/{id}` | `watermelon_messages_get` | Get a specific message |
| 10 | GET | `/fields` | `watermelon_fields_list` | List custom field definitions |
| 11 | POST | `/webhooks` | `watermelon_webhooks_create` | Create a webhook |
| 12 | PUT | `/webhooks/{id}` | `watermelon_webhooks_update` | Update a webhook |
| 13 | DELETE | `/webhooks/{id}` | `watermelon_webhooks_delete` | Delete a webhook |

**Coverage: 100% of the public API is exposed via MCP tools.**

## What's NOT in the Public API

These Watermelon platform features have no public API endpoints:

| Feature | Impact | Notes |
|---------|--------|-------|
| **Chatbot configuration** | Cannot create/modify/deploy chatbots via API | Must use Watermelon dashboard |
| **AI agent settings** | Cannot configure AI behavior, training data, or prompts | Dashboard only |
| **Analytics & reporting** | No access to conversation metrics, CSAT scores, response times | No data export |
| **Channel management** | Cannot add/remove channels (WhatsApp, web widget, etc.) | Dashboard setup required |
| **Team/agent management** | Cannot manage human agents, teams, or routing rules | Dashboard only |
| **Knowledge base** | Cannot manage FAQ items or knowledge base content | Dashboard only |
| **Automation rules** | Cannot create or manage workflow automations | Dashboard only |
| **Billing & plan info** | No access to subscription or usage data | N/A via API |
| **Widget customization** | Cannot configure chat widget appearance | Dashboard only |
| **Tags & categories** | No tag management endpoints | Likely internal only |
| **Conversation assignment** | Cannot assign/reassign conversations to agents | Major gap for automation |
| **Conversation status** | Cannot close/reopen/archive conversations | Limits workflow automation |

## Recommendations for API Extensions

Priority extensions that would significantly increase MCP server utility:

1. **Conversation lifecycle** — Close, reopen, assign, tag conversations. This is the #1 gap for building automated customer support workflows.
2. **Analytics read access** — Conversation volume, response times, CSAT scores. Essential for reporting and monitoring use cases.
3. **Knowledge base CRUD** — Create/update/delete FAQ items. Would enable AI-assisted knowledge base management.
4. **Chatbot configuration** — At minimum, read access to chatbot settings. Ideally, the ability to update AI prompts and training data.
5. **Webhook event types documentation** — The API allows creating webhooks but doesn't clearly document available event types.

## Rate Limits

- 100 concurrent requests per source
- 500 requests per minute
- HTTP 429 on limit exceeded
