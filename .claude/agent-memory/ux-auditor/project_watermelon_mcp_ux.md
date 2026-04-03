---
name: project_watermelon_mcp_ux
description: UX analysis context for Watermelon MCP server — API surface, personas, gaps, and workflow patterns
type: project
---

Watermelon MCP exposes 13 tools covering 100% of the current public API: contacts CRUD+search, conversations read-only (list/get with messages), messages send+get, fields list, webhooks CRUD.

**Key API gaps that constrain UX:**
- Cannot close/reopen/assign conversations (biggest automation blocker)
- No analytics/reporting endpoints
- No knowledge base access
- No chatbot/AI configuration
- Webhook event types not documented in API

**Personas identified:** Support agents (daily use), support managers (reporting/oversight), developers/automation builders (webhook/integration), AI orchestration pipelines (autonomous response drafting).

**Most compelling use cases:**
1. Intelligent triage assistant — list conversations, fetch full thread, draft reply, send (multi-tool chain)
2. Contact enrichment — search contact, update with CRM data via custom fields
3. Weekly digest — list all conversations, summarize with Claude, post to Slack
4. Webhook orchestration setup — create event hooks pointing to n8n/Zapier
5. Autonomous first-response drafting (with human approval step)

**Why: Referenced during use case analysis conversation on 2026-03-23.**
**How to apply: Use when advising on README improvements, tool descriptions, or future API extension priorities.**
