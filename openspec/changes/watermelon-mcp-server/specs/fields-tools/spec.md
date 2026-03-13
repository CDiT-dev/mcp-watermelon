## ADDED Requirements

### Requirement: List custom fields tool
The system SHALL register an MCP tool `watermelon_fields_list` that retrieves all custom field definitions via `GET /fields`.

#### Scenario: List all custom fields
- **WHEN** the tool is called
- **THEN** the system SHALL return all available custom field definitions

#### Scenario: No custom fields defined
- **WHEN** the organization has no custom fields
- **THEN** the system SHALL return an empty list (not an error)
