## Purpose

Protects opportunity uploads and contract files through explicit audience selection and access-checked storage and delivery throughout the workflow.

## ADDED Requirements

### Requirement: Opportunity uploads are private by default
Any authenticated portal customer SHALL be able to upload a document for their own opportunity without contractor verification. Files SHALL default to customer-private. Sharing a file into one negotiation SHALL authorize only that conversation's participants; listing publication, contact, company membership or another contractor's invitation SHALL NOT publish or share the file. Workspace documents SHALL be separate from negotiation documents and require effective work authorization.

#### Scenario: Customer uploads before contacting anyone
- **WHEN** a portal customer uploads a contract draft to their opportunity
- **THEN** only the customer and authorized administrators can read it until the customer explicitly chooses a permitted audience

#### Scenario: Share with A only
- **WHEN** a customer shares a draft into A's negotiation and separately invites B
- **THEN** A can download that shared draft, while B and anonymous visitors cannot

### Requirement: Uploads and relinking enforce ownership and audience
The system SHALL validate upload size, accepted content types and filename handling, reject unsafe active content, and prevent supplied resource identifiers, attachment identifiers, public flags or tokens from changing ownership or audience. Reusing an attachment SHALL require source-read and destination-write/share authority. A customer SHALL NOT share another customer's file. User-controlled file content SHALL never execute in the portal origin.

#### Scenario: Relink a protected file
- **WHEN** a participant tries to attach another customer's attachment identifier to their own readable conversation
- **THEN** the operation is rejected and neither source nor destination access changes

#### Scenario: Invalid upload
- **WHEN** an upload exceeds the documented limit or has a prohibited content type
- **THEN** it is rejected with a useful error and no readable orphan attachment remains

### Requirement: Every download rechecks effective access
Downloads, previews, binary fields and native attachment routes SHALL enforce current parent-document and audience access. Protected files SHALL have no public or bearer-token bypass. Revoking sharing or work access SHALL deny subsequent access through old URLs and sessions. Denials SHALL not disclose private filenames, record names or existence.

#### Scenario: Old URL after revocation
- **WHEN** the customer revokes a file share and the recipient retries the same download URL
- **THEN** the download is denied without returning file bytes or private metadata

#### Scenario: Native binary endpoint
- **WHEN** an unrelated user requests a protected file through the native binary route rather than the workflow page
- **THEN** access is denied under the same policy
