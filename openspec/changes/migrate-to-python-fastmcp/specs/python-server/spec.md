## ADDED Requirements

### Requirement: FastMCP server entry point
The server SHALL be a FastMCP 3.x application created in `src/watermelon_mcp/server.py`. It SHALL register all tools from the domain-specific tool modules and run via stdio transport.

#### Scenario: Server starts successfully
- **WHEN** the server is launched with valid `WATERMELON_API_KEY` and `WATERMELON_SECRET_KEY` environment variables
- **THEN** the FastMCP server starts on stdio transport and all 13 tools are registered

#### Scenario: Server fails without credentials
- **WHEN** the server is launched without `WATERMELON_API_KEY` or `WATERMELON_SECRET_KEY`
- **THEN** the server SHALL raise a validation error at startup before accepting connections

### Requirement: pyproject.toml with hatchling build
The project SHALL use `pyproject.toml` with hatchling as the build backend, following the mcp-things convention. It SHALL declare `fastmcp>=3.1.0`, `httpx>=0.28.1`, and `pydantic-settings>=2.12.0` as dependencies.

#### Scenario: Package installs cleanly
- **WHEN** a user runs `uv pip install -e .` in the project root
- **THEN** the package and all dependencies install without errors

### Requirement: Script entry point
The project SHALL define a `server` script entry point in `pyproject.toml` pointing to `watermelon_mcp.server:main`.

#### Scenario: Running via entry point
- **WHEN** a user runs the `server` command after installation
- **THEN** the MCP server starts on stdio transport
