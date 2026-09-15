## Purpose

Makes every business-critical marketplace transition traceable: when it happened, who performed it and, where judgment was involved, why. The audit trail stays internal, so it does not leak into public or portal-readable data.

## ADDED Requirements

### Requirement: Transition timestamps
The system SHALL record these server-generated times when the corresponding transitions happen:
- **job**: publication, assignment, latest delivery, completion, cancellation;
- **proposal**: submission, and the decision time when it leaves `submitted`;
- **review**: submission;
- **contractor profile**: suspension.

No caller SHALL be able to supply or alter these timestamps.

#### Scenario: Supplied timestamp rejected
- **WHEN** a customer calls update-job with a publication time in its input
- **THEN** the call is rejected and the publication time is unchanged

#### Scenario: Server time recorded
- **WHEN** a customer publishes a draft job
- **THEN** the recorded publication time is the server's time of the transition

### Requirement: Tracked changes on key fields
The system SHALL record an audit entry, with the acting user and the time, whenever any of these fields changes:
- **job**: state, visibility, budget, assigned contractor;
- **proposal**: state, amount, pricing type, estimated duration;
- **contractor profile**: status, publication, verification;
- **review**: hidden flag.

Each entry SHALL show the old and new values.

#### Scenario: Proposal amount revision is traceable
- **WHEN** a contractor changes their submitted proposal amount from 1000 to 800
- **THEN** the proposal's audit trail contains an entry by that contractor showing 1000 → 800

### Requirement: Reasons are recorded for judgment-based transitions
The system SHALL store, and add to the audit trail with actor and time, the reason given for each of these:
- job cancellation, by any role;
- change requests;
- manager resolution of a delivered job;
- profile suspension and reinstatement;
- review hiding and unhiding;
- proposal decline, when a reason is given.

#### Scenario: Manager force-completion reason
- **WHEN** a marketplace manager resolves a delivered job to done with a reason
- **THEN** the job's audit trail contains that reason, attributed to the manager

### Requirement: Real actor attribution
Audit entries SHALL name the user who invoked the operation. An operation that needs elevated privileges internally SHALL still attribute the entry to that user, not to a system or superuser identity.

#### Scenario: Portal acceptance attributed to customer
- **WHEN** a portal customer accepts a proposal
- **THEN** the audit entries for the job's and proposals' state changes name that customer as the author

### Requirement: Audit trail is internal
Audit entries SHALL be readable by marketplace managers. They SHALL NOT be returned to anonymous visitors or portal users when those users read record messages. Participants learn about transitions from the record's own state, timestamp, and note fields that their access allows.

#### Scenario: Contractor reads job messages
- **WHEN** the assigned contractor reads the messages of their `in_progress` job
- **THEN** no internal audit entry is returned

### Requirement: Audit records are durable
A job, proposal, or review that has left its initial state SHALL NOT be deletable, so its audit trail is preserved. The deletion rules in `marketplace-access-control` apply.

#### Scenario: Cancelled job with history
- **WHEN** a marketplace manager attempts to delete a `cancelled` job
- **THEN** the deletion is rejected and its audit trail remains
