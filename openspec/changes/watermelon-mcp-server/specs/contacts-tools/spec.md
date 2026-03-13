## ADDED Requirements

### Requirement: Create contact tool
The system SHALL register an MCP tool `watermelon_contacts_create` that creates a new contact via `POST /contacts`.

#### Scenario: Create contact with fields
- **WHEN** the tool is called with contact data (e.g., name, email, custom fields)
- **THEN** the system SHALL send a POST request to `/contacts` with the provided data and return the created contact

#### Scenario: Invalid contact data
- **WHEN** the API returns a 400 error for invalid data
- **THEN** the tool SHALL return an error result with the API error message

### Requirement: Get contact tool
The system SHALL register an MCP tool `watermelon_contacts_get` that retrieves a specific contact via `GET /contacts/{id}`.

#### Scenario: Get existing contact
- **WHEN** the tool is called with a valid contact ID
- **THEN** the system SHALL return the contact details including custom fields

#### Scenario: Contact not found
- **WHEN** the tool is called with a non-existent contact ID
- **THEN** the tool SHALL return an error result indicating the contact was not found

### Requirement: List contacts tool
The system SHALL register an MCP tool `watermelon_contacts_list` that retrieves all contacts via `GET /contacts`.

#### Scenario: List all contacts
- **WHEN** the tool is called
- **THEN** the system SHALL return the list of all contacts with their fields

### Requirement: Update contact tool
The system SHALL register an MCP tool `watermelon_contacts_update` that modifies a contact via `PUT /contacts/{id}`.

#### Scenario: Update contact fields
- **WHEN** the tool is called with a contact ID and updated field values
- **THEN** the system SHALL send a PUT request and return the updated contact

#### Scenario: Update non-existent contact
- **WHEN** the tool is called with an ID that does not exist
- **THEN** the tool SHALL return an error result

### Requirement: Search contacts tool
The system SHALL register an MCP tool `watermelon_contacts_search` that searches contacts via `GET /contacts/search`.

#### Scenario: Search with query
- **WHEN** the tool is called with search parameters
- **THEN** the system SHALL return matching contacts

#### Scenario: No results found
- **WHEN** the search query matches no contacts
- **THEN** the system SHALL return an empty result set (not an error)
