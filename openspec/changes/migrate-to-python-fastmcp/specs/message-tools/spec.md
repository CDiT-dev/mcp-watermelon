## ADDED Requirements

### Requirement: watermelon_messages_send tool
The system SHALL provide a `watermelon_messages_send` tool that sends a message via POST `/messages`.

#### Scenario: Send a message
- **WHEN** called with `data` containing message content and target
- **THEN** the tool sends POST `/messages` and returns the sent message as JSON text

### Requirement: watermelon_messages_get tool
The system SHALL provide a `watermelon_messages_get` tool that retrieves a message by ID via GET `/messages/{id}`.

#### Scenario: Get message by ID
- **WHEN** called with a valid `id`
- **THEN** the tool returns the message data as JSON text
