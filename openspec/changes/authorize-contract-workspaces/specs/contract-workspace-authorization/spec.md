## Purpose

Connects customer acceptance to exact protected work access and a reliable active-contract list without exposing unrelated Project or database resources.

## ADDED Requirements

### Requirement: Customer explicitly authorizes exact agreed work
Only the opportunity's owning customer SHALL accept the current structured offer and explicitly authorize its contractor to work on that contract. The decision SHALL include the displayed price, pricing type, currency, duration and offer revision and SHALL require affirmative work authorization. An administrator SHALL NOT authorize on the customer's behalf. The contractor SHALL have active internal approval and an active eligible profile; portal negotiation alone SHALL remain possible without these work prerequisites.

#### Scenario: Accept and authorize
- **WHEN** the customer confirms the current terms and explicitly authorizes an approved contractor
- **THEN** the system records that exact agreement and customer authorization and grants only that contract's work access

#### Scenario: Acceptance without authorization
- **WHEN** a caller invokes acceptance without affirmative work authorization, including through the old RPC operation
- **THEN** no assignment or workspace grant is created and a clear validation error is returned

#### Scenario: Contractor not approved for internal work
- **WHEN** the customer attempts work authorization for a portal-only contractor
- **THEN** authorization is refused without altering the offer and the customer is shown the pending prerequisite

### Requirement: Acceptance and access activation are atomic
Offer acceptance, closing competitors, creating or linking the dedicated workspace, recording frozen terms and activating the exact grants SHALL commit together or not at all. Concurrent acceptances SHALL produce at most one winning contractor and one workspace. Repeated requests for the same completed decision SHALL not duplicate workspace resources. Revocation or suspension racing with authorization SHALL never leave effective access for an ineligible account.

#### Scenario: Grant creation fails
- **WHEN** an acceptance cannot create its permitted workspace or grants
- **THEN** the job remains open, proposals remain unchanged and no partial resource or grant persists

#### Scenario: Two competing acceptances
- **WHEN** the customer concurrently accepts two offers for one opportunity
- **THEN** at most one wins and only that contractor receives one authorized workspace

#### Scenario: Approval revoked during acceptance
- **WHEN** administrator revocation races with customer acceptance
- **THEN** the final committed state contains no effective work grant for the revoked user

### Requirement: Each contract has a dedicated protected workspace
The initial workflow SHALL create a dedicated Project workspace per authorized contract, using native projects/tasks for execution and the existing contractor classification for reporting. Existing unrelated customer projects SHALL NOT be implicitly shared or imported. Only the customer, the authorized contractor within granted operations, and authorized administrators SHALL read the workspace. Adding tasks/resources SHALL require explicit association with the authorized contract and SHALL not expose unrelated parent, sibling or linked data. Project-stage changes SHALL NOT alter the commercial agreement or grant new access.

#### Scenario: Two contracts for the same customer
- **WHEN** A is authorized for contract C1 and B for C2
- **THEN** each contractor can operate only within their own contract, even though the customer and company match

#### Scenario: Contractor follows another project
- **WHEN** A becomes a follower or assignee on an unrelated project outside C1
- **THEN** no additional access is granted

#### Scenario: Task stage moved to done
- **WHEN** an authorized task is moved to a done stage
- **THEN** the opportunity remains governed by its delivery and customer-confirmation operations

### Requirement: Work operations are limited and auditable
Authorized contractors SHALL read contract terms, read authorized tasks and shared execution documents, update task execution status, post participant execution messages and submit deliverables. They SHALL NOT alter customer identity, agreement, prices, grants, company, project privacy, assignees, resource ownership or internal administrative notes, and SHALL NOT create/delete unrelated records. Customers SHALL use owner-scoped domain operations for review, changes, completion and revocation without broad Project write access. Participant execution communication SHALL be separate from administrative audit.

#### Scenario: Contractor changes price or privacy
- **WHEN** the authorized contractor tries to change the agreed price or make the project public
- **THEN** the request is rejected and effective permissions remain unchanged

#### Scenario: Legitimate delivery
- **WHEN** the authorized contractor posts an execution message and submits a permitted deliverable
- **THEN** only that contract's customer, current authorized contractor and administrators can read it

### Requirement: Revocation and terminal states control effective work access
The customer SHALL be able to revoke work authorization with a recorded reason; administrators SHALL be able to revoke for security with a reason, but not assign a replacement. Revocation SHALL remove all protected workspace/file access immediately, preserve the agreement/audit and private negotiation history, and prevent further execution operations until a fresh customer authorization. Completion SHALL end writable work access and remove the contract from active work; a still-approved, non-revoked contractor SHALL retain read-only completed-work access. Cancellation SHALL remove protected workspace access. Administrative account revocation or profile suspension SHALL override all retained work access. Reauthorization SHALL require the same eligible contractor and unchanged agreed terms; changing contractor requires a separately specified workflow.

#### Scenario: Customer revokes access mid-work
- **WHEN** the customer revokes A's authorization
- **THEN** A disappears from effective work grants and cannot use cached lists, Project RPC, messages or file URLs for that workspace

#### Scenario: Complete a contract
- **WHEN** the customer confirms delivery as complete
- **THEN** it leaves active work, task edits are denied, and eligible participants can read permitted completed work

#### Scenario: Suspend profile after assignment
- **WHEN** a manager suspends the assigned contractor's profile
- **THEN** the agreement remains historical but effective workspace access stops and reinstatement alone does not revive revoked grants

### Requirement: Active contracts reflect authorization rather than contact
A contractor's active-contract list SHALL contain exactly their non-revoked, effectively authorized contracts in progress or awaiting delivery confirmation. Contacted, negotiating, declined, lost, cancelled, completed and inaccessible contracts SHALL be excluded. List counts, search, pagination, backend navigation and direct resource access SHALL agree for both newly approved and existing sessions.

#### Scenario: Mixed contractor history
- **WHEN** A has two invitations, one submitted proposal, one authorized in-progress contract, one completed contract and one revoked contract
- **THEN** A's active list and count show exactly the one authorized in-progress contract
