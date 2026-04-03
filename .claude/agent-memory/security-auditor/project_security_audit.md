---
name: mcp-watermelon security audit (March 2026)
description: Findings from the first comprehensive security audit — key issues were npm publish scope and .gitignore gaps, not credential leakage
type: project
---

Audit performed 2026-03-16. Server sits behind Keycloak; focus was application-layer security.

**Key findings:**
1. No hardcoded secrets in code or git history — credentials handled correctly via env vars
2. npm `files` field not set + no `.npmignore` → `npm publish` would include `.claude/` dirs and `openspec/` docs (LOW risk, but messy)
3. `.gitignore` does not exclude `.env` files → if a developer creates `.env` for local testing it could be committed accidentally (MEDIUM)
4. `dist/` is correctly gitignored but not npmignored — compiled output ships without being a problem since it's the deliverable
5. `z.record(z.string(), z.unknown())` used as input schema for create/update/send tools — passes all data through to Watermelon API with no structural validation (LOW, by design for pass-through tools)
6. `String(e)` error passthrough in all tools — error messages from Watermelon API (status code + response body) are returned to MCP client; no token in those messages but API error bodies could contain PII (MEDIUM)
7. `watermelon_contacts_list` and `watermelon_conversations_list` have no pagination — could flood LLM context with large PII datasets (MEDIUM)
8. Webhook `data` field accepts any URL with no validation — no SSRF risk (all calls go to Watermelon's own API, not the user-supplied URL), but misconfigured webhook URLs would not be caught at MCP layer

**npm audit:** 0 vulnerabilities across 94 dependencies.

**Python migration notes for design.md:**
- pydantic-settings is the right call for env var validation
- httpx async client: remember to set `follow_redirects=False` and appropriate timeouts
- Add `files` field to `pyproject.toml` when publishing to PyPI to avoid including dev docs

**Why:** This was a first audit before the Python migration to establish a baseline.
**How to apply:** Reference these findings when reviewing the Python migration implementation to ensure issues aren't re-introduced.
