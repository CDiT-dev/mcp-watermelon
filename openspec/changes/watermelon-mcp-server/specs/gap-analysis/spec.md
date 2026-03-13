## ADDED Requirements

### Requirement: Gap analysis document
The project SHALL include a `GAP_ANALYSIS.md` document in the repository root that documents the coverage and limitations of the Watermelon public API.

#### Scenario: Document lists all available endpoints
- **WHEN** a reader views the gap analysis
- **THEN** they SHALL see all 13 public API endpoints with their capabilities

#### Scenario: Document identifies missing capabilities
- **WHEN** a reader views the gap analysis
- **THEN** they SHALL see a list of Watermelon platform features that are NOT accessible via the public API (e.g., analytics, chatbot configuration, channel management, user management, AI agent settings)

#### Scenario: Document includes recommendations
- **WHEN** a reader views the gap analysis
- **THEN** they SHALL see recommendations for API extensions that would increase MCP server utility
