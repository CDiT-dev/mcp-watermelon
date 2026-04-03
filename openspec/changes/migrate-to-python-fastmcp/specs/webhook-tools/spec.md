## ADDED Requirements

### Requirement: watermelon_webhooks_create tool
The system SHALL provide a `watermelon_webhooks_create` tool that creates a webhook via POST `/webhooks`.

#### Scenario: Create webhook
- **WHEN** called with `data` containing webhook configuration
- **THEN** the tool sends POST `/webhooks` and returns the created webhook as JSON text

### Requirement: watermelon_webhooks_update tool
The system SHALL provide a `watermelon_webhooks_update` tool that updates a webhook via PUT `/webhooks/{id}`.

#### Scenario: Update webhook
- **WHEN** called with `id` and `data` containing updated settings
- **THEN** the tool sends PUT `/webhooks/{id}` and returns the updated webhook as JSON text

### Requirement: watermelon_webhooks_delete tool
The system SHALL provide a `watermelon_webhooks_delete` tool that deletes a webhook via DELETE `/webhooks/{id}`.

#### Scenario: Delete webhook
- **WHEN** called with a valid `id`
- **THEN** the tool sends DELETE `/webhooks/{id}` and returns a success message
