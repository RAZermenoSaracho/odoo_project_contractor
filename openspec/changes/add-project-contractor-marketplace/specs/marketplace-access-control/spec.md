## Purpose

Defines who can read and change marketplace data at the ORM/RPC boundary, independently of any website or portal controller. It covers per-actor access, record scoping, field-level privacy, protected lifecycle fields, enumeration resistance, and the chatter and attachment exposure of marketplace records.

## ADDED Requirements

### Requirement: Actors and roles
The system SHALL recognize these actors:
- **anonymous visitor**: the public user;
- **authenticated user**: any logged-in portal user or internal user without marketplace manager rights;
- **customer**: the individual contact who owns a job; other contacts of the same company or commercial entity are not customers of that job;
- **contractor**: a contact with a marketplace profile;
- **assigned contractor**: the contractor assigned to a job;
- **proposal owner**: the contractor who submitted a proposal;
- **marketplace manager**: members of a dedicated internal group;
- **administrator**: settings administrators, who SHALL also be marketplace managers.

Customer, contractor, assigned contractor and proposal owner SHALL be derived from marketplace records at the time of each access. They SHALL NOT be user groups that could be granted independently of those records. Internal users without the marketplace manager group SHALL get the same marketplace actor permissions as authenticated portal users, subject to company scope and any installed restricted-account ceiling. This rule grants no access outside the marketplace.

#### Scenario: Internal employee is not privileged
- **WHEN** an internal user without the marketplace manager group searches proposals
- **THEN** only proposals they submitted or that were submitted to their own jobs are returned

#### Scenario: Administrator is a manager
- **WHEN** a settings administrator reads marketplace records
- **THEN** they have the same access as a marketplace manager

### Requirement: Read access matrix
Read access SHALL follow this matrix intersected with the company and installed account-isolation policies; the "Everyone" column covers anonymous visitors and every authenticated user:

| Record | Everyone | Additionally, authenticated users | Participants | Marketplace manager |
| --- | --- | --- | --- | --- |
| Job | `open` + visibility `public` | `open` + visibility `portal` | the customer: all their jobs; the assigned contractor: jobs assigned to them | all |
| Proposal | none | none | the proposal owner and the job's customer | all |
| Contractor profile | `active` + published | none extra | the owner: their own profile in any status | all |
| Skill catalog | all | all | — | all |

#### Scenario: Anonymous visitor reads a portal-only job
- **WHEN** an anonymous visitor searches for jobs
- **THEN** jobs with visibility `portal` are not returned

#### Scenario: Owner reads own draft profile
- **WHEN** a portal user reads their own `draft` contractor profile
- **THEN** the profile is returned

#### Scenario: Other user reads a draft profile
- **WHEN** a portal user reads another user's `draft` profile by identifier
- **THEN** access is denied

### Requirement: No generic mutation for non-managers
Anonymous visitors, authenticated portal users and internal users without the marketplace manager group SHALL NOT be able to create, update or delete any marketplace record through generic ORM or RPC operations. All their changes SHALL go through the explicit domain operations defined in `marketplace-domain-api`.

#### Scenario: Portal generic create
- **WHEN** a portal user calls the generic create operation on the proposal model through RPC
- **THEN** the call is rejected with an access error and no proposal is created

#### Scenario: Portal generic write to own draft job
- **WHEN** a portal user calls the generic write operation on their own draft job to change its title
- **THEN** the call is rejected with an access error

### Requirement: Protected fields are changeable only through domain operations
These fields SHALL be rejected in any generic create or update by any caller, including marketplace managers and administrators:
- **job**: state, customer, company, reference, assigned contractor, accepted proposal, every lifecycle timestamp, cancellation role and reason, delivery note, change-request reason, revision count;
- **proposal**: job, contractor, state, close reason, decline reason, submission and decision times;
- **contractor profile**: partner, status, publication, verification, suspension reason and suspension timestamp.

The domain operations SHALL still be able to change these fields as their specifications allow. Manager edits to non-protected content SHALL obey the same lifecycle and pending-proposal edit locks; manager access SHALL NOT bypass those invariants.

#### Scenario: Manager generic write to profile verification
- **WHEN** a marketplace manager generically writes a profile verification flag
- **THEN** the call is rejected and the verification flag is unchanged

#### Scenario: Manager edits non-protected field
- **WHEN** a marketplace manager calls the generic write operation to fix a typo in an open job's title when it has no submitted proposals
- **THEN** the title changes

### Requirement: Private identity data is not disclosed through readable fields
For any reader who is not authorized to know them, the system SHALL NOT disclose these values through any readable field, related value, display name, or record metadata (creator, last editor, followers):
- a job's customer;
- a profile's partner.

Only marketplace managers SHALL be able to read the partner references of customers and profiles directly. Participants SHALL receive only the display-level information their specifications grant.

#### Scenario: Metadata leakage on a public job
- **WHEN** an anonymous visitor reads every field they are allowed to read on a public `open` job, including creator and last-editor fields
- **THEN** no returned value identifies or names the customer

### Requirement: Enumeration resistance
Searches and counts on marketplace records SHALL include only records the caller can read. For a caller who cannot read a marketplace record, every marketplace domain operation that targets it by identifier SHALL fail with the same outcome as when no record has that identifier. Error messages from generic reads SHALL NOT disclose the content of a record the caller cannot read, including its display name. A record's display name SHALL NOT contain customer identity, contractor partner identity, proposal amounts, or proposal messages.

#### Scenario: Guessing proposal identifiers through search
- **WHEN** a portal user searches proposals whose identifiers fall in a range of sequential values
- **THEN** only their own proposals and proposals to their own jobs are returned

#### Scenario: Domain operation on a guessed identifier
- **WHEN** a portal user calls withdraw-proposal with the identifier of an existing proposal owned by another contractor, and again with an identifier that matches no proposal
- **THEN** both calls fail with the same error category and an equivalent message

#### Scenario: Proposal display name is neutral
- **WHEN** an internal user without manager rights triggers an access error on another contractor's proposal
- **THEN** the error discloses neither the proposal's amount nor its message nor the contractor's partner

### Requirement: Attachments are refused on marketplace records in v1
The system SHALL refuse to create or re-link file attachments to jobs, proposals or contractor profiles, whoever the caller and whatever the record's state, including participant-only states such as `in_progress`. This prevents a file attached to a record from becoming readable by everyone who can read that record, for example on a public job. v1 SHALL NOT relax this refusal for any flow.

#### Scenario: Manager attaches a file to an open job
- **WHEN** a marketplace manager attempts to attach a file to an `open` public job
- **THEN** the attachment is rejected

#### Scenario: Participant attaches a deliverable to an in-progress job
- **WHEN** the assigned contractor or the customer attempts, by any route, to attach a file to their `in_progress` job or to its accepted proposal
- **THEN** the attachment is rejected

### Requirement: Chatter is internal-only in v1
Jobs, proposals and contractor profiles SHALL each carry an internal audit and discussion thread. Only marketplace managers SHALL be able to post on it. Messages that non-manager participants (including restricted internal users) or anonymous visitors can read SHALL NOT include audit entries, tracked-value changes, or internal notes. Customers and contractors SHALL NOT be automatically added as followers.

#### Scenario: Portal user posts on a public job
- **WHEN** a portal user attempts to post a message on an `open` public job
- **THEN** the post is rejected

#### Scenario: Portal user reads job messages
- **WHEN** a portal user reads the messages of a job they can read
- **THEN** no audit entry, tracked-value change, or internal note is returned

### Requirement: No participant messaging on core audit records
The core addon SHALL NOT provide participant messaging on its listing, proposal or profile audit threads. Those threads and directly attached files SHALL remain closed to participant messaging even when a frontend is installed. A separately specified negotiation/workspace extension SHALL provide its own private participant channels and document policies; it SHALL NOT make the core audit stream participant-readable. The core alone is not the complete contractor workflow.
#### Scenario: Assigned contractor cannot post on their job
- **WHEN** the assigned contractor attempts to post a message on their `in_progress` job
- **THEN** the post is rejected

#### Scenario: Customer cannot message a proposal's contractor
- **WHEN** a job's customer attempts to post a message on a proposal submitted to their job
- **THEN** the post is rejected

### Requirement: Deletion is restricted
Only marketplace managers SHALL be able to delete marketplace records. They SHALL be limited to:
- `draft` jobs that have never had a proposal;
- contractor profiles that are not referenced by any job or proposal;
- catalog entries that are not referenced.

Proposals SHALL NOT be deletable by anyone through generic operations.

#### Scenario: Delete a done job
- **WHEN** a marketplace manager attempts to delete a `done` job
- **THEN** the deletion is rejected

#### Scenario: Delete a proposal
- **WHEN** a marketplace manager attempts to delete a proposal
- **THEN** the deletion is rejected

### Requirement: Company scope intersects actor permissions
Jobs SHALL have a server-derived company within the customer's permitted workflow company scope. Contractors SHALL not bid or be assigned outside their permitted company scope. Actor rules SHALL never bypass company restrictions, including through supplied context. Public listings SHALL expose only deliberate published content, not company-private metadata. Cross-company collaboration requires a separately specified policy.

#### Scenario: Contractor from another company
- **WHEN** a contractor attempts to submit a proposal for work outside their permitted workflow companies
- **THEN** the operation is rejected even if they know the listing identifier

#### Scenario: Supplied company on creation
- **WHEN** a customer includes an unauthorized company or expanded company context in job creation
- **THEN** no job is created outside their permitted company scope
