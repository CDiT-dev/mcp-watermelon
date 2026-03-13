## ADDED Requirements

### Requirement: Send message tool
The system SHALL register an MCP tool `watermelon_messages_send` that sends a new message via `POST /messages`.

#### Scenario: Send message successfully
- **WHEN** the tool is called with message content and a conversation/contact target
- **THEN** the system SHALL send a POST request to `/messages` and return the created message

#### Scenario: Send fails with invalid data
- **WHEN** the API returns a 400 error
- **THEN** the tool SHALL return an error result with the API error message

### Requirement: Get message tool
The system SHALL register an MCP tool `watermelon_messages_get` that retrieves a specific message via `GET /messages/{id}`.

#### Scenario: Get existing message
- **WHEN** the tool is called with a valid message ID
- **THEN** the system SHALL return the message details

#### Scenario: Message not found
- **WHEN** the tool is called with a non-existent message ID
- **THEN** the tool SHALL return an error result
