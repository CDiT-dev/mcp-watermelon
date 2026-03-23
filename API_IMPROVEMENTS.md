# Watermelon Public API — Improvement Recommendations

**From:** Casey Romkes, CDIT (https://cdit.de)
**Context:** We built an open-source MCP server ([github.com/CDiT-dev/mcp-watermelon](https://github.com/CDiT-dev/mcp-watermelon)) that connects Watermelon to AI assistants like Claude, ChatGPT, and Copilot. During development and end-to-end testing against the live API, we identified several improvements that would unlock significantly more value for your customers using AI-powered support workflows.

This document is written for your engineering team. Every item is grounded in real testing against your production API.

---

## What works well

Before getting to improvements: your API is solid for what it covers.

- **Authentication** (Bearer `api_key.secret_key`) is simple and clean.
- **Contact CRUD** is reliable — create, get, list, update, search all work as documented.
- **Custom fields system** is well-designed — the `/fields` endpoint makes it easy to discover available fields and their types before creating contacts.
- **Webhook system** works and the `action_id`/`entity_id`/`verb_id` model is flexible.
- **Rate limits** (500/min, 100 concurrent) are generous for integration use cases.
- **204 responses** for empty results and successful updates are correctly implemented.

---

## 1. Conversation lifecycle management (highest impact)

**Current state:** The API can list and read conversations (`GET /all/conversations`, `GET /conversations/{id}`) and send messages (`POST /messages`). But there is no way to close, reopen, assign, or tag a conversation.

**What this blocks:** Every AI-powered support workflow is incomplete. An AI assistant can read a customer's question, draft a response, and send it — but then the ticket stays open. The human agent still has to open the Watermelon dashboard to close it. This means the API can never fully automate a support interaction end-to-end.

**Recommendation:**
```
PATCH /conversations/{id}
{
  "is_closed": true,        // close the conversation
  "team_id": 42,            // reassign to a different team
  "archived": "2026-03-23"  // archive it
}
```

This single endpoint would unlock:
- AI agents that fully resolve and close simple tickets autonomously
- Smart routing: AI reads the question, assigns to the right team
- Automated archival of resolved conversations

This is the #1 feature that would make AI integrations production-ready.

---

## 2. Webhook event type documentation

**Current state:** The webhook create endpoint requires `action_id`, `entity_id`, and `verb_id` as integers. The docs explain the mapping:
- `action_id`: create=1, update=2, delete=3, archive=4, forward-team=5, forward-agent=6
- `entity_id`: conversation=1, contact=2, field=3, message=5
- `verb_id`: GET=1, PUT=2, POST=3, DELETE=4

**The problem:** This is not discoverable from the API itself. An AI assistant (or a developer using an AI coding tool) cannot look up valid combinations without reading the docs. There is also no endpoint to list existing webhooks (`GET /webhooks` returns 405).

**Recommendation:**
1. Add `GET /webhooks` — list all registered webhooks for the company. Without this, there is no way to check for duplicate subscriptions or audit what's configured.
2. Add `GET /webhooks/events` (or include in `/fields`) — return the valid action/entity/verb combinations. This makes the webhook system self-documenting.

---

## 3. Conversation filtering by contact

**Current state:** `GET /all/conversations` supports `page`, `limit`, `from`, and `to` filters. There is no way to filter by contact/caller.

**What this blocks:** The most common AI support workflow is: "Show me all conversations with this customer." Currently this requires fetching *all* conversations and filtering client-side, which is slow and wasteful at scale.

**Recommendation:**
```
GET /all/conversations?caller_id=12345&limit=25&page=0
```

A single query parameter. This would reduce a multi-step, high-latency operation to a single API call.

---

## 4. Message sending — clarify user_id requirement

**Current state:** `POST /messages` requires `user_id` (integer). This is the Watermelon user/agent ID who sends the message. The docs list it as required, but there is no API endpoint to discover valid user IDs.

**The problem:** When an AI assistant wants to send a message, it needs a `user_id` but has no way to find one. The integration builder has to hardcode an agent ID or look it up in the dashboard manually.

**Recommendation:** Either:
1. Add `GET /users` or `GET /agents` — list the company's agents with their IDs, or
2. Allow `user_id` to be optional — if omitted, attribute the message to "API / Bot" (similar to how the chatbot sends messages today)

Option 2 is simpler and probably what most integrations want.

---

## 5. Contact deletion

**Current state:** `DELETE /contacts/{id}` returns 405 (Method Not Allowed). Contacts can only be created and updated, never deleted.

**The problem:** During development, automated testing, and GDPR compliance (right to erasure), the inability to delete contacts is a constraint. Test contacts accumulate in the account with no cleanup path.

**Recommendation:** Add `DELETE /contacts/{id}` with a 204 response. If full deletion is not possible, consider a soft-delete or anonymize endpoint that clears PII while preserving conversation history — this is important for GDPR (DSGVO) compliance in the EU market.

---

## 6. Pagination consistency

**Current state:** Most endpoints use `page` (0-based) + `limit`, which is clean and consistent. However, the contact search endpoint (`GET /contacts/search`) doesn't document a `fieldId` parameter, even though it works when provided. The conversations list endpoint uses a different path (`/all/conversations`) than the single-conversation endpoint (`/conversations/{id}`).

**Recommendation:**
- Document the `fieldId` parameter on search (it works and is useful)
- Consider aligning paths: `/conversations` for list, `/conversations/{id}` for detail (the `/all/` prefix is unexpected)
- All list endpoints should return a consistent envelope: `{ "data": [...], "total": N, "page": 0, "limit": 25 }` — this makes pagination predictable without trial-and-error

---

## 7. OpenAPI spec accessibility

**Current state:** The `llms.txt` file at `watermelon.ai/docs/llms.txt` correctly points to `docs/public_api_openapi3.yml`, but that URL returns 404. The JSON variant (`docs/api-reference/openapi.json`) also appears unavailable.

**Recommendation:** Publish the OpenAPI spec at a stable URL. This enables:
- Automatic SDK generation for any language
- AI coding tools (Cursor, Claude, Copilot) to understand your API without manual docs reading
- Postman/Insomnia collection import

A working OpenAPI spec is the single highest-leverage developer experience improvement you can ship. Every tool in the ecosystem consumes it.

---

## Summary — prioritized

| # | Improvement | Effort | Impact for AI integrations |
|---|---|---|---|
| 1 | Conversation lifecycle (close/assign) | Medium | Unlocks end-to-end AI support automation |
| 2 | GET /webhooks + event discovery | Low | Prevents duplicate webhooks, enables self-service |
| 3 | Conversation filter by caller_id | Low | Eliminates N+1 queries for customer history |
| 4 | User/agent listing or optional user_id | Low | Removes hardcoded IDs from integrations |
| 5 | Contact deletion | Low | GDPR compliance, test cleanup |
| 6 | Pagination consistency + path alignment | Low | Better developer experience |
| 7 | Published OpenAPI spec | Low | Enables entire ecosystem of auto-generated tools |

Items 2, 3, 4, 6, and 7 are likely small changes. Item 1 is the strategic one — it's the difference between "AI can help with support" and "AI can handle support."

---

*We'd welcome the opportunity to maintain the official MCP integration and expand it as your API evolves. Contact: casey@cdit.de*
