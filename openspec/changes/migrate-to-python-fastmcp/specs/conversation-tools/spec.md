## ADDED Requirements

### Requirement: watermelon_conversations_list tool
The system SHALL provide a `watermelon_conversations_list` tool that lists all conversations via GET `/conversations`.

#### Scenario: List all conversations
- **WHEN** called with no parameters
- **THEN** the tool returns all conversations as JSON text

### Requirement: watermelon_conversations_get tool
The system SHALL provide a `watermelon_conversations_get` tool that retrieves a specific conversation via GET `/conversations/{id}`.

#### Scenario: Get conversation by ID
- **WHEN** called with a valid `id`
- **THEN** the tool returns the conversation with its messages as JSON text
