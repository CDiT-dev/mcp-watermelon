## ADDED Requirements

### Requirement: List conversations tool
The system SHALL register an MCP tool `watermelon_conversations_list` that retrieves all conversations via `GET /conversations`.

#### Scenario: List all conversations
- **WHEN** the tool is called
- **THEN** the system SHALL return all company conversations

### Requirement: Get conversation tool
The system SHALL register an MCP tool `watermelon_conversations_get` that retrieves a specific conversation via `GET /conversations/{id}`.

#### Scenario: Get existing conversation
- **WHEN** the tool is called with a valid conversation ID
- **THEN** the system SHALL return the conversation details including messages

#### Scenario: Conversation not found
- **WHEN** the tool is called with a non-existent conversation ID
- **THEN** the tool SHALL return an error result
