## ADDED Requirements

### Requirement: Portal users can activate Contractor access
An authenticated portal user SHALL be able to activate Contractor access for
their own existing user and partner through a CSRF-protected website action.
Activation SHALL make that user internal and add the Contractor group. It SHALL
NOT create a second user or partner.

#### Scenario: Portal identity is retained
- **WHEN** a portal user activates Contractor access
- **THEN** the same user and partner become a Contractor internal identity

### Requirement: Contractor Project access is assignment-scoped
Contractors SHALL have read and write, but not create or delete, access to
Projects and Tasks. They SHALL see projects and tasks assigned to their user or
partner contractor, plus projects with no contractor or assignee. Projects and
tasks assigned only to someone else SHALL not be readable.

#### Scenario: Assigned and unassigned projects
- **WHEN** a Contractor searches projects with one own assignment, one other
  assignment, and one project without assignments
- **THEN** only the own and unassigned projects are returned

### Requirement: Contractors can edit only their own contact
A Contractor SHALL read and write only `user.partner_id` on `res.partner` and
SHALL NOT create or delete contact records.

#### Scenario: Foreign contact is denied
- **WHEN** a Contractor reads or edits another user's contact
- **THEN** the operation is denied

### Requirement: Website contract pages honor ORM security
The addon SHALL provide authenticated website pages for Contractor activation
and visible contracts. Contract pages SHALL query through the current request
environment and SHALL NOT use sudo to broaden project visibility.

#### Scenario: Website list matches the record rule
- **WHEN** a Contractor opens the contract list
- **THEN** it contains only projects the Contractor can search through the ORM
