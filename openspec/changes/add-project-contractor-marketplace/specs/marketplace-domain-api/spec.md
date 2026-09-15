## Purpose

Defines the frontend-independent operation contract that presentation addons, backend views, RPC clients and future modules use to act on the marketplace. It covers the operation inventory, how the acting party is determined, input allowlisting, error behavior, read helpers, dependency direction, and independence from deployment topology.

## ADDED Requirements

### Requirement: Operation inventory
The marketplace SHALL expose these explicit operations. Each operation SHALL be callable over RPC by the actors listed and SHALL enforce its own authorization and preconditions.

| Operation | Actor |
| --- | --- |
| Create own marketplace profile; update own profile; activate own profile; publish / unpublish own profile | Authenticated user (profile owner) |
| Suspend / reinstate profile; set / clear verification; unpublish any profile | Marketplace manager |
| Create job; update job; publish job; unpublish job; cancel job (pre-assignment) | Customer |
| Submit proposal; update proposal; withdraw proposal | Contractor (proposal owner) |
| Decline proposal; accept proposal | Customer only (no manager or administrator equivalent exists) |
| Mark delivered | Assigned contractor |
| Request changes; confirm completion | Customer |
| Cancel job (post-assignment) | Customer, assigned contractor |
| Cancel job (any non-terminal state); resolve delivered job to done | Marketplace manager |
| Submit review | Customer of a `done` job |
| Hide / unhide review | Marketplace manager |

Every state transition in the other marketplace specifications SHALL be reachable only through one of these operations. The v1 inventory SHALL NOT include operations for participant messaging, file attachments, automatic completion, contractor-to-customer reviews, or accepting proposals on a customer's behalf. The internal helpers that operations use (for example closing competing proposals or recording transitions) SHALL NOT be callable over RPC.

#### Scenario: Internal helper not remotely callable
- **WHEN** a portal user calls, over RPC, the internal helper that closes competing proposals on a job
- **THEN** the call is refused and nothing changes

#### Scenario: Operation available over RPC
- **WHEN** an authenticated portal user with an `active` profile calls the submit-proposal operation over RPC with valid input for an `open` job
- **THEN** the proposal is created exactly as it would be through any other client

### Requirement: The acting party is derived, never supplied
Every operation SHALL determine the acting customer, contractor, reviewer or manager from the authenticated calling user. No operation SHALL accept an identifier of the acting party, or of an ownership or assignment relation, as input.

#### Scenario: Supplying an acting-party identifier
- **WHEN** a caller includes a customer, contractor or reviewer identifier in an operation's input
- **THEN** the operation is rejected and nothing is written

### Requirement: Strict input allowlists
Each operation that accepts values SHALL accept only its documented field set:
- **profile create/update**: public name, headline, biography, skills, hourly rate and its currency, availability, country;
- **job create/update**: the v1 editable job fields, including currency and visibility;
- **proposal submit/update**: message, pricing type, amount, estimated duration;
- **decline**: optional reason;
- **deliver**: optional note;
- **request changes, and every cancel, suspend, hide or resolve operation**: a reason;
- **review submit**: rating and comment.

An input containing any other key SHALL be rejected as a whole, with nothing written. Unknown keys SHALL NOT be silently ignored. Relational inputs SHALL reference only records the caller can read.

#### Scenario: Unknown key
- **WHEN** a contractor calls update-proposal with an amount and an extra `state` key
- **THEN** the call is rejected and neither the amount nor the state changes

#### Scenario: Unreadable related record
- **WHEN** a customer calls create-job with a skill identifier that does not exist
- **THEN** the call is rejected and no job is created

### Requirement: Error semantics
Operations SHALL fail atomically: a failed operation writes nothing. Failures SHALL be distinguishable by category:
- **not found or not permitted**: the target record does not exist, the caller cannot read it, or the caller is not permitted to perform the operation on a record they can read. For records the caller cannot read, the result SHALL be indistinguishable from "does not exist".
- **invalid request**: input fails validation, or the record's current state does not allow the operation. The error SHALL carry a message suitable for display to the user.
- **concurrent modification**: the target changed or was locked by another transaction. The caller can retry or refresh.

#### Scenario: Wrong state
- **WHEN** a customer calls publish-job on an `open` job
- **THEN** the call fails with an invalid-request error carrying a displayable message

#### Scenario: Inaccessible record
- **WHEN** a portal user calls withdraw-proposal on a proposal owned by another contractor
- **THEN** the call fails with the same outcome as for a nonexistent proposal

### Requirement: Frontend independence
The marketplace SHALL be fully usable, with every operation and every guarantee intact, when no website, portal-page, or other presentation addon is installed. The marketplace addon SHALL NOT define HTTP routes, website or portal templates, portal URLs, navigation, branding or theming. It SHALL NOT depend on any presentation addon. Its guarantees SHALL hold for every caller acting as the requesting user, whatever route or client issued the call.

#### Scenario: Installed without frontend
- **WHEN** the marketplace addon is installed in a database without `website` or any presentation addon
- **THEN** installation succeeds and every operation behaves as specified when called through the ORM or RPC

### Requirement: Dependency direction
The marketplace addon SHALL depend only on the contractor foundation addon (`project_contractor`), and through it on Project. It SHALL NOT depend on any of:
- a website, portal-page, theme, or presentation addon;
- any deployment-specific or glue addon;
- `sale`, `account`, or `rating`;
- any hosting, tenant-provisioning, or SSO module.

Presentation addons SHALL depend on the marketplace addon, never the reverse. The foundation addon SHALL NOT depend on the marketplace addon, and no dependency cycle SHALL exist.

#### Scenario: Declared dependencies
- **WHEN** the marketplace addon's declared dependencies are inspected
- **THEN** they are exactly `project_contractor`

#### Scenario: Foundation usable without the marketplace
- **WHEN** only the foundation addon is installed
- **THEN** it installs and works without any marketplace model

### Requirement: Independence from deployment topology
The marketplace addon SHALL be installable and fully functional in any database, whatever the database's name, hostname, subdomain, or role in a hosting topology. It SHALL NOT refuse installation, hide functionality, or reject operations because of such properties. Deployment policy (which databases run the marketplace) SHALL be decided outside the addon.

#### Scenario: Arbitrarily named database
- **WHEN** the marketplace addon is installed in a database named `marketplace_demo`
- **THEN** installation succeeds and every operation behaves as specified

#### Scenario: No topology check during operations
- **WHEN** a domain operation runs in any database
- **THEN** its outcome depends only on its specified authorization, preconditions and input

### Requirement: Marketplace jobs are the marketplace's source of truth; integrations are additive
Marketplace jobs, proposals and reviews SHALL be the sole source of truth for the marketplace lifecycle. The complete lifecycle SHALL work without Sales, Accounting, or hosting modules installed. No record of another business model, including project tasks and their stages, SHALL drive a marketplace state transition. In v1 the marketplace SHALL NOT create or modify project tasks. Future integrations, such as handing an accepted job off to a project task, SHALL be optional, explicit additions that consume marketplace records without replacing or bypassing the domain operations.

#### Scenario: Full lifecycle without Sales
- **WHEN** the marketplace addon is installed without `sale` or `account` and a job goes from creation to review
- **THEN** every step succeeds through the domain operations alone

#### Scenario: Task stages do not drive jobs
- **WHEN** a project task that mentions a job is moved to a done stage
- **THEN** the job's state is unchanged

### Requirement: Read surface for clients
Clients SHALL read marketplace data through ordinary search and read operations as the requesting user, subject to `marketplace-access-control`. Jobs SHALL expose these per-caller read helpers:
- whether the caller is the job's customer (also usable as a search filter);
- whether the caller is the assigned contractor (also usable as a search filter);
- the caller's own active proposal on the job, if any;
- the number of proposals on the job, visible only to the customer and managers;
- the customer's display name, provided only to participants and managers.

Marketplace profiles SHALL expose whether the profile belongs to the caller.

#### Scenario: My Jobs listing
- **WHEN** a portal user searches jobs filtered on "caller is customer"
- **THEN** exactly the jobs they own are returned, in every state

#### Scenario: My proposal on a job
- **WHEN** a contractor with a `submitted` proposal reads an `open` job
- **THEN** the job's "my proposal" helper refers to that proposal

#### Scenario: Customer display name hidden from non-participants
- **WHEN** a non-participant portal user reads the customer display name helper on an `open` job
- **THEN** the value is empty
