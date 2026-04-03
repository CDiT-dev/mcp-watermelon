## ADDED Requirements

### Requirement: watermelon_fields_list tool
The system SHALL provide a `watermelon_fields_list` tool that lists all custom field definitions via GET `/fields`.

#### Scenario: List all fields
- **WHEN** called with no parameters
- **THEN** the tool returns all custom field definitions as JSON text
