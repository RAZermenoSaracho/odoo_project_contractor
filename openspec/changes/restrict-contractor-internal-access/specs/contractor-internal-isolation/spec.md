## Purpose

Allows approved contractors to use a narrowly restricted internal account without inheriting access to unrelated database records or business applications.

## ADDED Requirements

### Requirement: Restricted internal status is an access ceiling
A restricted contractor SHALL receive no business-record access merely from becoming internal. Every read or operation SHALL require an explicit supported policy and, for protected work, a current record-specific grant. The restriction SHALL apply in addition to upstream rights across backend, portal, ORM, RPC, reports, exports, searches and counts. A user-supplied context, group membership, assignee, follower, company or commercial relationship SHALL NOT bypass it. Ordinary employees who are not restricted contractors SHALL retain their existing rights.

#### Scenario: Internal contractor with no grants
- **WHEN** a newly approved restricted contractor searches employee-visible projects, tasks, contacts and business records
- **THEN** no unrelated business records are returned and direct reads and mutations of them are denied

#### Scenario: Upstream permissive group cannot widen access
- **WHEN** a restricted contractor follows an unrelated project or acquires an additional implied Project group
- **THEN** effective access remains bounded by explicit grants, or the incompatible group change is rejected atomically

#### Scenario: Ordinary employee regression
- **WHEN** an ordinary employee reads records they could read before this layer was installed
- **THEN** their access remains unchanged

### Requirement: Supported database policy is explicit and fails closed
The system SHALL maintain a reviewed policy for every model reachable by a restricted user on the supported installation. Business records without a policy SHALL be inaccessible. Safe bootstrap/reference data and own-account fields SHALL be explicitly limited to what the workflow needs. Approval SHALL be refused if the installed module/group/route combination has not passed compatibility checks. Installing a module or changing security configuration SHALL NOT silently broaden existing contractors' access; unsupported combinations SHALL disable their protected-work operations until reviewed.

#### Scenario: Additional application adds internal access
- **WHEN** a newly installed module grants all internal users read access to its business model and no contractor policy covers it
- **THEN** restricted contractors cannot read that model and compatibility status prevents unsafe protected-work use

#### Scenario: Safe own-account access
- **WHEN** a restricted contractor opens their preferences and the workflow's currency or language selector
- **THEN** only approved own-account fields and reference values are available, without a general user or contact directory

### Requirement: Effective grants are exact and revocable
A work grant SHALL identify the database-local user, authorized resource, allowed operations, company and validity. Authorization of one task SHALL NOT imply authorization of sibling tasks, a parent contract, other customers, shared folders or another company. Grant administration SHALL be private to trusted workflow operations and designated administrators; contractors SHALL NOT create, modify, transfer or reactivate grants. Revocation SHALL take effect for subsequent reads and writes, including in existing sessions, cached lists and file downloads.

#### Scenario: One of two tasks authorized
- **WHEN** contractor A is authorized for task T1 but not T2 in the same company or project
- **THEN** T1 is accessible within its granted operations and T2 is absent from reads, searches, counts, exports and name lookup

#### Scenario: Revocation in an existing session
- **WHEN** a grant is revoked and the contractor reuses an existing session or bookmarked resource URL
- **THEN** the next access is denied, even if a follower or assignee relation remains

#### Scenario: Forged grant and company context
- **WHEN** a contractor submits a generic grant write or expands allowed-company context beyond their authorization
- **THEN** the request is rejected without widening access

### Requirement: Related data and indirect channels obey the same boundary
The restriction SHALL cover related fields and display names, mail messages, followers, activities, attachments, download tokens, report models and aggregate results. Protected files SHALL NOT become public or accessible solely through an old access token. A contractor SHALL NOT discover private contact identities, unrelated internal notes or other users' record existence through these channels.

#### Scenario: Attachment and chatter probe
- **WHEN** a contractor guesses a file or message identifier belonging to an unauthorized contract
- **THEN** content, filename, author, record name and existence are not disclosed by the workflow's responses

#### Scenario: Count and report probe
- **WHEN** a contractor requests grouped task counts or a report spanning all projects
- **THEN** only authorized records contribute, or the unsupported report is refused

### Requirement: Account transitions preserve the ceiling
Only designated administrators SHALL enable or disable restricted internal access through audited operations. Transition into the role SHALL preserve the existing user and partner identity, set a minimal reviewed group/company configuration atomically, and refuse privilege conflicts. Removing the restriction while leaving the person as an ordinary internal user SHALL require a separate explicit employee-conversion operation outside the contractor workflow. Revoking contractor internal access SHALL return workflow-managed accounts to portal and revoke work grants atomically.

#### Scenario: Attempted self-promotion
- **WHEN** a contractor uses RPC to change user type, groups, companies or restriction status
- **THEN** the call is denied and the account remains unchanged

#### Scenario: Restriction removal without demotion
- **WHEN** an administrator attempts to remove the contractor restriction while retaining ordinary internal rights through the contractor workflow
- **THEN** the unsafe transition is refused
