## ADDED Requirements

### Requirement: Async HTTP client for Watermelon API
The system SHALL provide a `WatermelonClient` class using `httpx.AsyncClient` that handles authentication and request/response for the Watermelon.ai API at `https://public.watermelon.ai`.

#### Scenario: Authenticated request
- **WHEN** a tool calls `client.get("/contacts")`
- **THEN** the client sends a GET request with `Authorization: Bearer {api_key}.{secret_key}` header and `Content-Type: application/json`

#### Scenario: API error handling
- **WHEN** the Watermelon API returns a non-2xx status code
- **THEN** the client SHALL raise an exception containing the status code and response body

#### Scenario: Rate limit handling
- **WHEN** the Watermelon API returns HTTP 429
- **THEN** the client SHALL raise a specific error indicating rate limiting

### Requirement: HTTP methods
The client SHALL support GET, POST, PUT, and DELETE methods matching the current TypeScript client's interface.

#### Scenario: POST with JSON body
- **WHEN** a tool calls `client.post("/contacts", data={"name": "Test"})`
- **THEN** the client sends a POST request with the data serialized as JSON in the request body

#### Scenario: DELETE returning no content
- **WHEN** a DELETE request returns HTTP 204
- **THEN** the client SHALL return `None` without attempting to parse a response body
