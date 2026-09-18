## Purpose

Guarantees that a marketplace job is assigned to exactly one contractor, through the customer's acceptance of exactly one of that job's proposals. The acceptance is atomic and safe under concurrent requests. It cannot be forged through direct record writes or manipulated identifiers.

## ADDED Requirements

### Requirement: Only the customer accepts, and only a valid proposal
Only the job's customer SHALL be able to accept a proposal. It can be accepted only when all of these hold:
- the proposal is `submitted`;
- the proposal belongs to that job;
- the job is `open`;
- the proposal's contractor profile is `active`.

A contractor SHALL NOT be able to accept any proposal, including their own.

Accepting a proposal is exclusively the customer's business decision. No marketplace manager or administrator SHALL be able to accept a proposal, select a contractor, or assign a job on a customer's behalf. No manager operation, group permission, backend action, or generic write SHALL provide an equivalent path. Any future exceptional administrative assignment workflow SHALL be introduced only as its own explicitly specified operation, never as a side effect of manager access rights.

#### Scenario: Customer accepts a submitted proposal
- **WHEN** the customer accepts a `submitted` proposal on their `open` job
- **THEN** the acceptance succeeds

#### Scenario: Contractor self-assignment
- **WHEN** a contractor attempts to accept their own proposal
- **THEN** the request fails exactly as if the operation were not permitted for them, and nothing changes

#### Scenario: Marketplace manager attempts acceptance
- **WHEN** a marketplace manager who is not the job customer and can read the proposal calls the accept-proposal operation on a `submitted` proposal of an `open` job
- **THEN** the request is rejected as not permitted, and the job and every proposal are unchanged

#### Scenario: Administrator attempts acceptance
- **WHEN** a settings administrator who is not the job customer calls the accept-proposal operation on a `submitted` proposal of an `open` job
- **THEN** the request is rejected as not permitted, and nothing changes

#### Scenario: Suspended contractor
- **WHEN** the customer accepts a proposal whose contractor profile was suspended after submission
- **THEN** the request is rejected because the proposal is no longer `submitted`

#### Scenario: Other customer's proposal
- **WHEN** customer X attempts to accept a proposal that belongs to customer Y's job
- **THEN** the request fails exactly as if the proposal did not exist

### Requirement: Acceptance is atomic
Accepting a proposal SHALL, in a single all-or-nothing operation:
1. move the proposal to `accepted` and record its decision time;
2. move the job from `open` to `in_progress`;
3. set the job's assigned contractor to the proposal's contractor;
4. set the job's accepted proposal to that proposal;
5. record the job's assignment time;
6. move every other `submitted` proposal on the job to `closed`, with close reason `job_filled`, and record their decision times.

If any step fails, no step's effect SHALL persist.

#### Scenario: Competing proposals are closed
- **WHEN** the customer accepts proposal P1 on a job that also has `submitted` proposals P2 and P3 and `withdrawn` proposal P4
- **THEN** P1 is `accepted`, the job is `in_progress` with P1's contractor assigned
- **AND** P2 and P3 are `closed` with reason `job_filled`
- **AND** P4 is unchanged

#### Scenario: Failure leaves no partial state
- **WHEN** an acceptance fails after its preconditions were checked (for example, a constraint violation while closing competitors)
- **THEN** the job remains `open`, P1 remains `submitted`, and no competing proposal changes state

### Requirement: At most one accepted proposal per job under concurrency
The system SHALL guarantee that a job never has more than one `accepted` proposal, and never more than one assigned contractor, even when acceptance requests for the same job arrive at the same time. The system SHALL re-check every acceptance precondition after it has exclusive access to the job. It SHALL enforce the one-accepted-proposal rule at the storage level as well as in the operation. A request that loses the race SHALL fail without side effects, with a result that tells the caller the job changed and the action may be retried or reviewed.

#### Scenario: Two simultaneous acceptances
- **WHEN** the customer accepts proposal P1 and proposal P2 on the same `open` job in two concurrent requests
- **THEN** exactly one request succeeds
- **AND** the other fails without changing any record
- **AND** the job ends with exactly one accepted proposal and one assigned contractor

#### Scenario: Acceptance after job left open
- **WHEN** the customer accepts a proposal on a job that was cancelled in a transaction committed just before
- **THEN** the request is rejected and the proposal stays `closed`

### Requirement: Assignment cannot be set outside acceptance
A job's assigned contractor, its accepted proposal, its assignment time and its move to `in_progress` SHALL change only through proposal acceptance. Generic record creation or updates from any caller, including marketplace managers and administrators using ordinary ORM or RPC writes, SHALL be rejected when they try to set or change these fields.

#### Scenario: Portal RPC write to assignment
- **WHEN** a portal user sends a generic write that sets a job's assigned contractor to their own profile
- **THEN** the write is rejected and the job is unchanged

#### Scenario: Manager generic write to state
- **WHEN** a marketplace manager sends a generic write setting an `open` job's state to `in_progress`
- **THEN** the write is rejected

### Requirement: Accepted terms are frozen
Once a proposal is accepted, its pricing type, amount, currency and estimated duration SHALL become the job's agreed terms. They SHALL NOT be modifiable by any actor afterwards.

#### Scenario: Agreed terms readable by participants
- **WHEN** the assigned contractor or the customer reads the job's accepted proposal
- **THEN** they see the accepted pricing type, amount, currency and estimated duration

### Requirement: Core assignment does not grant protected work access
Standalone marketplace acceptance SHALL record the commercial assignment only, never create users or grant Project access. When negotiation and workspace extensions are installed, this same acceptance transaction SHALL enforce their revision, explicit authorization and eligibility requirements before any assignment persists.

#### Scenario: Standalone core acceptance
- **WHEN** a customer accepts an eligible proposal with only the marketplace core installed
- **THEN** the commercial assignment is recorded but no Project task, collaborator, internal account or work grant is created
