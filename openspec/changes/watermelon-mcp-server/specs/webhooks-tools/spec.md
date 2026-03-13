## ADDED Requirements

### Requirement: Create webhook tool
The system SHALL register an MCP tool `watermelon_webhooks_create` that creates a new webhook via `POST /webhooks`.

#### Scenario: Create webhook successfully
- **WHEN** the tool is called with a callback URL and event triggers
- **THEN** the system SHALL create the webhook and return the webhook object with its ID

#### Scenario: Invalid webhook configuration
- **WHEN** the API returns a 400 error for invalid configuration
- **THEN** the tool SHALL return an error result

### Requirement: Update webhook tool
The system SHALL register an MCP tool `watermelon_webhooks_update` that modifies a webhook via `PUT /webhooks/{id}`.

#### Scenario: Update webhook settings
- **WHEN** the tool is called with a webhook ID and updated settings
- **THEN** the system SHALL update the webhook and return the updated object

#### Scenario: Webhook not found
- **WHEN** the tool is called with a non-existent webhook ID
- **THEN** the tool SHALL return an error result

### Requirement: Delete webhook tool
The system SHALL register an MCP tool `watermelon_webhooks_delete` that removes a webhook via `DELETE /webhooks/{id}`.

#### Scenario: Delete existing webhook
- **WHEN** the tool is called with a valid webhook ID
- **THEN** the system SHALL delete the webhook and return a confirmation

#### Scenario: Delete non-existent webhook
- **WHEN** the tool is called with a non-existent webhook ID
- **THEN** the tool SHALL return an error result
