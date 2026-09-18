## Purpose

Defines the marketplace job: a customer's public or logged-in listing of work they want an external contractor to perform. It covers ownership, minimum v1 content and currency, visibility, and the lifecycle up to assignment (drafting, publishing, editing, unpublishing and cancellation).

## ADDED Requirements

### Requirement: Job creation by an authenticated customer
Any authenticated user who is not the public user SHALL be able to create a marketplace job without contractor application, approval, verification or profile requirements. The system SHALL set the job's customer to the calling user's contact and SHALL reject any input that tries to set a different customer. A new job SHALL start in state `draft` and SHALL receive a unique, immutable, human-readable reference.

#### Scenario: Portal user creates a draft job
- **WHEN** an authenticated portal user creates a job with a title
- **THEN** a job in state `draft` is created with that user's contact as customer and a unique reference

#### Scenario: Customer cannot be spoofed
- **WHEN** a portal user submits job creation input that names another contact as customer
- **THEN** the request is rejected and no job is created

#### Scenario: Anonymous visitor cannot create jobs
- **WHEN** an unauthenticated visitor attempts to create a job
- **THEN** the request is rejected

### Requirement: Jobs are owned by the individual contact
In v1 a job SHALL be owned by exactly one individual contact: the contact of the user who created it. Customer rights (reading drafts, editing, publishing, unpublishing, cancelling, deciding on proposals, confirming completion) SHALL belong only to that contact. Other contacts SHALL NOT receive customer rights through a shared company, parent contact, or commercial entity. Company-level ownership is outside v1.

#### Scenario: Colleague at the same company is not the customer
- **WHEN** portal user B, whose contact belongs to the same company as the customer's contact, attempts to read the customer's `draft` job or publish it
- **THEN** the read fails exactly as if the job did not exist and the job stays `draft`

#### Scenario: Colleague cannot decide on proposals
- **WHEN** a contact of the same company as the customer attempts to accept or decline a proposal on the customer's `open` job
- **THEN** the request is rejected and no proposal changes state

### Requirement: Minimum v1 job content
A job SHALL support these customer-editable fields:
- title (required, at most 120 characters);
- description (plain text);
- required skills;
- pricing preference (`fixed` or `hourly`);
- optional minimum and maximum budget, in the job's currency;
- currency;
- expected duration (`less_than_week`, `one_to_four_weeks`, `one_to_three_months`, `more_than_three_months`);
- visibility (`public` or `portal`).

Budget values SHALL be non-negative, and the minimum SHALL NOT exceed the maximum when both are set. Domain-specific classifications (for example software versions or industry work types) are not part of the generic v1 job; deployments express them as skills.

#### Scenario: Invalid budget range
- **WHEN** a customer saves a job with minimum budget 500 and maximum budget 100
- **THEN** the request is rejected and the job is unchanged

#### Scenario: Deferred field is not accepted
- **WHEN** a customer submits job input containing a field outside the v1 editable set (for example an access password or an attachment)
- **THEN** the request is rejected and nothing is written

### Requirement: Job currency
A job's monetary values SHALL be expressed in the job's currency, which SHALL be a reference to a standard Odoo currency record. When the customer supplies no currency, the job SHALL use the currency of the job's company. The customer SHALL be able to choose any active currency, and the domain SHALL NOT be structurally restricted to the company currency. Choosing an inactive currency SHALL be rejected.

#### Scenario: Company currency by default
- **WHEN** a customer creates a job without a currency in a company whose currency is USD
- **THEN** the job's currency is USD

#### Scenario: Customer chooses another active currency
- **WHEN** a customer creates a job with currency EUR, which is active but is not the company currency
- **THEN** the job is created with currency EUR and its budget is expressed in EUR

#### Scenario: Inactive currency rejected
- **WHEN** a customer creates a job with a currency that is not active
- **THEN** the request is rejected and no job is created

### Requirement: Jobs never store external credentials
A job SHALL NOT have any field meant for credentials, passwords, API keys, or connection secrets for external systems.

#### Scenario: No credential fields exist
- **WHEN** the job's field definitions are inspected
- **THEN** no field is defined for storing credentials, passwords, tokens, or connection details

### Requirement: Default and explicit job visibility
A job created without a visibility value SHALL have visibility `portal` (authenticated users only). Only the customer SHALL be able to set visibility `public`, and only as an explicit choice, at creation or through an update the edit rules permit. No transition or other operation SHALL widen a job's visibility implicitly.

#### Scenario: Visibility defaults to logged-in only
- **WHEN** a customer creates and publishes a job without specifying visibility
- **THEN** the job's visibility is `portal` and anonymous visitors cannot read it

#### Scenario: Customer explicitly chooses public visibility
- **WHEN** a customer creates a job with visibility `public` and publishes it
- **THEN** anonymous visitors can read the `open` job

#### Scenario: Publishing does not widen visibility
- **WHEN** a customer publishes a `draft` job whose visibility is `portal`
- **THEN** its visibility is still `portal`

### Requirement: Publishing a job
The job's customer SHALL be able to publish a `draft` job, which moves it to `open` and records the publication time. Publishing SHALL require a title, a description, and a pricing preference. No other actor SHALL be able to publish a customer's job.

#### Scenario: Publish complete draft
- **WHEN** the customer publishes a `draft` job with title, description and pricing preference
- **THEN** the job becomes `open` and its publication time is recorded

#### Scenario: Publish incomplete draft
- **WHEN** the customer publishes a `draft` job with no description
- **THEN** the request is rejected and the job stays `draft`

#### Scenario: Another user cannot publish
- **WHEN** a different portal user attempts to publish someone else's draft job
- **THEN** the request fails exactly as if the job did not exist, and the job stays `draft`

### Requirement: Job visibility by state and visibility setting
Job read access SHALL be:
- a `draft` job is readable only by its customer and marketplace managers;
- an `open` job with visibility `public` is also readable by anonymous visitors and by every authenticated user;
- an `open` job with visibility `portal` is also readable by every authenticated user, but not by anonymous visitors;
- a job in any later state (`in_progress`, `delivered`, `done`, `cancelled`) is readable only by its customer, its assigned contractor (if any), and marketplace managers.

#### Scenario: Anonymous visitor browses public open jobs
- **WHEN** an anonymous visitor lists jobs
- **THEN** only `open` jobs with visibility `public` are returned

#### Scenario: Portal-only job hidden from anonymous visitors
- **WHEN** an anonymous visitor requests an `open` job with visibility `portal` by its identifier
- **THEN** the job is not returned

#### Scenario: Assigned job leaves the marketplace
- **WHEN** an `open` job becomes `in_progress`
- **THEN** authenticated users other than the customer, the assigned contractor and marketplace managers can no longer read it

### Requirement: Customer identity is private to participants
A job SHALL NOT reveal its customer's identity (contact, user, name, or contact data) to anyone other than the customer, the assigned contractor, and marketplace managers. This applies to every readable attribute of the job, including record-creator and last-editor metadata and follower information.

#### Scenario: Other contractor reads an open job
- **WHEN** a portal user who is not the customer reads every readable field of an `open` public job
- **THEN** no returned value identifies the customer's contact or user or contains the customer's name

#### Scenario: Assigned contractor sees customer name
- **WHEN** the assigned contractor reads an `in_progress` job
- **THEN** the customer's display name is available to them

### Requirement: Editing job details
The customer SHALL be able to update a job's editable fields while the job is `draft`. While it is `open`, they can edit only if the job has no proposal in state `submitted`. The lock SHALL apply uniformly to every editable field, including description, budget, currency and visibility; v1 SHALL NOT distinguish material from non-material fields. No actor SHALL be able to change a job's details once the job has left `open`. Nobody SHALL be able to change a job's customer or reference after creation.

#### Scenario: Edit open job before any proposal
- **WHEN** the customer updates the description of an `open` job with no submitted proposals
- **THEN** the description changes

#### Scenario: Edit locked by pending proposal
- **WHEN** the customer updates the budget of an `open` job that has one `submitted` proposal
- **THEN** the request is rejected and the budget is unchanged

#### Scenario: Lock applies to every editable field
- **WHEN** the customer updates only the title, only the currency, or only the visibility of an `open` job that has one `submitted` proposal
- **THEN** each request is rejected and the job is unchanged

#### Scenario: Lock lifts when no proposal is pending
- **WHEN** the only proposal on an `open` job has been withdrawn and the customer then updates the description
- **THEN** the description changes

#### Scenario: Edit after assignment
- **WHEN** the customer updates the title of an `in_progress` job
- **THEN** the request is rejected

### Requirement: Unpublishing a job
The customer SHALL be able to return an `open` job to `draft`, but only when it has no proposal in state `submitted`.

#### Scenario: Unpublish with pending proposals
- **WHEN** the customer unpublishes an `open` job that has a `submitted` proposal
- **THEN** the request is rejected and the job stays `open`

### Requirement: Cancellation before assignment
The customer or a marketplace manager SHALL be able to cancel a `draft` or `open` job, which moves it to `cancelled`. A reason is optional for the customer and required for a manager. Cancellation SHALL record the cancellation time, the reason, and whether the customer or a manager cancelled. In the same operation, every `submitted` proposal on the job SHALL become `closed` with close reason `job_cancelled`. `cancelled` SHALL be a terminal state.

#### Scenario: Customer cancels an open job with proposals
- **WHEN** the customer cancels an `open` job that has two `submitted` proposals and one `withdrawn` proposal
- **THEN** the job becomes `cancelled` with its cancellation time and role recorded
- **AND** both submitted proposals become `closed` with reason `job_cancelled`
- **AND** the withdrawn proposal is unchanged

#### Scenario: Cancelled job cannot be reopened
- **WHEN** anyone attempts to publish or edit a `cancelled` job
- **THEN** the request is rejected

### Requirement: Listings contain deliberately shared opportunity content only
A published job SHALL be an opportunity listing, not the protected customer workspace. Private uploads, negotiation history and execution resources SHALL remain in separately authorized records. Publishing or contacting a contractor SHALL NOT grant access to those resources. A separately specified negotiation extension can add an optional initial price and negotiability while retaining currency validation and the pending-proposal edit lock.

#### Scenario: Publish with private contract material
- **WHEN** a customer publishes the listing for an opportunity that also has private documents in the document extension
- **THEN** only the deliberately published listing fields become visible and the documents retain their explicit audiences
