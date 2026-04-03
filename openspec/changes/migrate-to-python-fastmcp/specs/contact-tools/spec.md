## ADDED Requirements

### Requirement: watermelon_contacts_create tool
The system SHALL provide a `watermelon_contacts_create` tool that creates a new contact via POST `/contacts`.

#### Scenario: Create contact with data
- **WHEN** called with `data` containing contact fields
- **THEN** the tool sends POST `/contacts` and returns the created contact as JSON text

### Requirement: watermelon_contacts_get tool
The system SHALL provide a `watermelon_contacts_get` tool that retrieves a contact by ID via GET `/contacts/{id}`.

#### Scenario: Get existing contact
- **WHEN** called with a valid `id`
- **THEN** the tool returns the contact data as JSON text

### Requirement: watermelon_contacts_list tool
The system SHALL provide a `watermelon_contacts_list` tool that lists all contacts via GET `/contacts`.

#### Scenario: List all contacts
- **WHEN** called with no parameters
- **THEN** the tool returns all contacts as JSON text

### Requirement: watermelon_contacts_update tool
The system SHALL provide a `watermelon_contacts_update` tool that updates a contact via PUT `/contacts/{id}`.

#### Scenario: Update contact fields
- **WHEN** called with `id` and `data` containing updated fields
- **THEN** the tool sends PUT `/contacts/{id}` and returns the updated contact as JSON text

### Requirement: watermelon_contacts_search tool
The system SHALL provide a `watermelon_contacts_search` tool that searches contacts via GET `/contacts/search?query={query}`.

#### Scenario: Search contacts
- **WHEN** called with a `query` string
- **THEN** the tool returns matching contacts as JSON text
