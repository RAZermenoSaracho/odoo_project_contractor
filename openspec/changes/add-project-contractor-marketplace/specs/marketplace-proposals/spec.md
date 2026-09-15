## Purpose

Lets eligible contractors offer to perform an open marketplace job. It governs who can submit, update, withdraw and decline proposals. It also guarantees that proposal content (amounts, messages and existence) stays private between the contractor, the job's customer and marketplace managers.

## ADDED Requirements

### Requirement: Proposal submission eligibility
A user SHALL be able to submit a proposal for a job only when all of these hold:
- the user's contact has a marketplace profile in status `active`; publication is not required;
- the job is `open` and readable by the user;
- the user's contact is not the job's customer and does not share the customer's commercial entity;
- the contractor has no other proposal on that job in state `submitted` or `accepted`;
- the contractor has no `declined` proposal on that job.

The system SHALL set the proposal's contractor to the caller's own profile and SHALL reject input naming another contractor.

Withdrawing their own proposal SHALL NOT, on its own, prevent a contractor from submitting again to the same job. Any later submission SHALL be checked against every eligibility condition above at the time it is made. A customer's decline SHALL permanently prevent that contractor from submitting again to that job, whatever happens to the job afterwards.

#### Scenario: Eligible contractor submits
- **WHEN** a portal user with an `active` profile submits a proposal to an `open` job they can read
- **THEN** a proposal in state `submitted` is created for their profile and the submission time is recorded

#### Scenario: No active profile
- **WHEN** a portal user whose profile is `draft` (or who has no profile) submits a proposal
- **THEN** the request is rejected

#### Scenario: Customer bids on own job
- **WHEN** the job's customer, who also has an `active` contractor profile, submits a proposal to that job
- **THEN** the request is rejected

#### Scenario: Duplicate active proposal
- **WHEN** a contractor with a `submitted` proposal on a job submits a second proposal to the same job
- **THEN** the request is rejected, including when both submissions arrive concurrently

#### Scenario: Resubmission after decline
- **WHEN** a contractor whose proposal on a job was `declined` submits a new proposal to that job
- **THEN** the request is rejected

#### Scenario: Decline still blocks after the job is republished
- **WHEN** a contractor's proposal was `declined`, the customer then unpublished and republished the job, and the contractor submits a new proposal
- **THEN** the request is rejected

#### Scenario: Resubmission after withdrawal
- **WHEN** a contractor whose only proposal on an `open` job is `withdrawn` submits a new proposal
- **THEN** a new `submitted` proposal is created

#### Scenario: Resubmission after withdrawal on a job that is no longer eligible
- **WHEN** a contractor withdrew their proposal and the job has since become `in_progress` or `cancelled`, and the contractor submits a new proposal
- **THEN** the request is rejected

#### Scenario: Proposal to a non-open job
- **WHEN** a contractor submits a proposal to a job that is `draft`, `in_progress`, `delivered`, `done`, or `cancelled`
- **THEN** the request is rejected

#### Scenario: Contractor spoofing
- **WHEN** a portal user submits proposal input naming another contractor's profile
- **THEN** the request is rejected and no proposal is created

### Requirement: Proposal content
A proposal SHALL contain:
- a message (required, plain text, at most 5000 characters);
- a pricing type (`fixed` or `hourly`);
- an amount strictly greater than zero, in the job's currency (a total for `fixed`, a rate for `hourly`);
- an estimated duration in whole days, at least 1.

The proposal's job and contractor SHALL be immutable after creation.

#### Scenario: Non-positive amount
- **WHEN** a contractor submits a proposal with amount 0
- **THEN** the request is rejected

#### Scenario: Currency follows the job
- **WHEN** a proposal is created for a job whose currency is EUR
- **THEN** the proposal's amount is expressed in EUR regardless of any currency in the input

### Requirement: Updating a submitted proposal
The proposal's contractor SHALL be able to update its message, pricing type, amount and estimated duration only while the proposal is `submitted` and its job is `open`. No other actor SHALL be able to modify proposal content.

#### Scenario: Contractor revises amount
- **WHEN** the contractor updates the amount of their `submitted` proposal on an `open` job
- **THEN** the amount changes and the change is recorded in the proposal's audit trail

#### Scenario: Customer cannot alter a proposal
- **WHEN** the job's customer attempts to change a proposal's amount
- **THEN** the request is rejected

#### Scenario: Accepted proposal is frozen
- **WHEN** the contractor attempts to update an `accepted` proposal
- **THEN** the request is rejected

### Requirement: Withdrawing a proposal
The proposal's contractor SHALL be able to withdraw it while it is `submitted`, which moves it to `withdrawn` and records the decision time. Accepted, declined and closed proposals SHALL NOT be withdrawable.

#### Scenario: Withdraw pending proposal
- **WHEN** the contractor withdraws their `submitted` proposal
- **THEN** the proposal becomes `withdrawn`

#### Scenario: Withdraw after acceptance
- **WHEN** the contractor attempts to withdraw an `accepted` proposal
- **THEN** the request is rejected

### Requirement: Declining a proposal
The job's customer SHALL be able to decline a `submitted` proposal on their `open` job, with an optional reason. Declining moves the proposal to `declined` and records the decision time. The contractor SHALL be able to read the decline reason.

#### Scenario: Customer declines
- **WHEN** the customer declines a `submitted` proposal with reason "Budget too high"
- **THEN** the proposal becomes `declined` and its contractor can read the reason

#### Scenario: Third party cannot decline
- **WHEN** a portal user who is neither the customer nor a manager attempts to decline a proposal
- **THEN** the request fails exactly as if the proposal did not exist

### Requirement: Proposal state machine
A proposal SHALL be in exactly one state: `submitted`, `accepted`, `declined`, `withdrawn`, or `closed`. The only allowed transitions SHALL be from `submitted` to one of the other four states. `accepted`, `declined`, `withdrawn` and `closed` SHALL be terminal. A `closed` proposal SHALL carry a close reason: `job_filled`, `job_cancelled`, or `contractor_suspended`. The system SHALL be the only actor that closes proposals, as a side effect of a job or profile transition.

#### Scenario: Terminal proposal cannot change state
- **WHEN** any actor, including a marketplace manager, attempts to move a `declined` proposal to `submitted`
- **THEN** the request is rejected

### Requirement: Proposal privacy
A proposal SHALL be readable only by its contractor, the customer of its job, and marketplace managers. Anyone else, including other contractors who bid on the same job and anonymous visitors, SHALL NOT be able to:
- read it;
- search it;
- count it;
- learn that it exists.

A job's visibility setting SHALL NOT affect proposal visibility. The number of proposals on a job SHALL be available only to the job's customer and marketplace managers.

#### Scenario: Competing contractor searches proposals
- **WHEN** contractor B searches for proposals on a public `open` job where contractor A has a `submitted` proposal
- **THEN** only contractor B's own proposals are returned and contractor A's amount and message are not disclosed

#### Scenario: Direct identifier access
- **WHEN** contractor B requests contractor A's proposal by its identifier
- **THEN** the request fails exactly as if the proposal did not exist

#### Scenario: Proposal count hidden from non-owners
- **WHEN** a contractor reads a public `open` job that has three proposals
- **THEN** the proposal count they see does not reveal the three proposals

#### Scenario: Customer sees all proposals to their job
- **WHEN** the customer lists proposals for their job
- **THEN** every proposal on that job is returned, whatever its state

#### Scenario: Anonymous visitor
- **WHEN** an anonymous visitor attempts to read any proposal
- **THEN** access is denied
