## ADDED Requirements

### Requirement: MCP server initialization
The system SHALL create an MCP server using `McpServer` from `@modelcontextprotocol/sdk` with name `mcp-watermelon` and connect via `StdioServerTransport`.

#### Scenario: Server starts successfully
- **WHEN** the server process is launched
- **THEN** the MCP server connects via stdio and is ready to accept tool calls

#### Scenario: Server logs to stderr
- **WHEN** the server needs to output diagnostic information
- **THEN** it SHALL use `console.error` (never `console.log`) to avoid corrupting the JSON-RPC protocol on stdout

### Requirement: Authentication via environment variables
The system SHALL read `WATERMELON_API_KEY` and `WATERMELON_SECRET_KEY` from environment variables and construct a Bearer token as `${apiKey}.${secretKey}`.

#### Scenario: Valid credentials provided
- **WHEN** both `WATERMELON_API_KEY` and `WATERMELON_SECRET_KEY` are set
- **THEN** all HTTP requests to the Watermelon API SHALL include the header `Authorization: Bearer <apiKey>.<secretKey>`

#### Scenario: Missing credentials
- **WHEN** either `WATERMELON_API_KEY` or `WATERMELON_SECRET_KEY` is not set
- **THEN** the server SHALL exit with a clear error message indicating which variable is missing

### Requirement: HTTP client for Watermelon API
The system SHALL provide a shared HTTP client that sends requests to `https://public.watermelon.ai` with the Bearer token and appropriate headers.

#### Scenario: Successful API call
- **WHEN** a tool makes an API request and receives a 200 response
- **THEN** the client SHALL return the parsed JSON response body

#### Scenario: API error response
- **WHEN** the Watermelon API returns a 4xx or 5xx status code
- **THEN** the tool SHALL return an MCP error result with `isError: true` and a descriptive message including the HTTP status code

#### Scenario: Network failure
- **WHEN** the HTTP request fails due to a network error
- **THEN** the tool SHALL return an MCP error result with `isError: true` and the error message

### Requirement: Rate limit handling
The system SHALL handle HTTP 429 responses from the Watermelon API.

#### Scenario: Rate limit exceeded
- **WHEN** the API returns status 429
- **THEN** the tool SHALL return an MCP error result with `isError: true` and a message indicating rate limit exceeded
