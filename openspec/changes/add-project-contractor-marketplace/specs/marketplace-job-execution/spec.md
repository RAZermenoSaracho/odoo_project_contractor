## Purpose

Defines how an assigned marketplace job runs from the start of work to delivery and customer-confirmed completion, or to cancellation. It records the timestamps that later completion metrics depend on.

## ADDED Requirements

### Requirement: Job state machine after assignment
After assignment a job SHALL be in exactly one of `in_progress`, `delivered`, `done`, or `cancelled`. The allowed transitions SHALL be:
- `in_progress` → `delivered`: by the assigned contractor.
- `delivered` → `in_progress`: by the customer (request changes), with a reason.
- `delivered` → `done`: by the customer (confirm completion), or by a marketplace manager with a reason.
- `in_progress` → `cancelled`: by the customer or the assigned contractor with a reason, or by a marketplace manager with a reason.
- `delivered` → `cancelled`: by a marketplace manager only, with a reason.

`done` and `cancelled` SHALL be terminal, and every other transition SHALL be rejected.

#### Scenario: Customer cannot skip delivery
- **WHEN** the customer attempts to confirm completion of an `in_progress` job
- **THEN** the request is rejected and the job stays `in_progress`

#### Scenario: Contractor cannot confirm own work
- **WHEN** the assigned contractor attempts to confirm completion of a `delivered` job
- **THEN** the request is rejected

#### Scenario: Terminal job
- **WHEN** any actor attempts any transition on a `done` job
- **THEN** the request is rejected

### Requirement: Marking work delivered
The assigned contractor SHALL be able to mark an `in_progress` job as delivered, with an optional delivery note. Doing so moves the job to `delivered` and records the delivery time; a later delivery replaces the delivery time and note. The customer SHALL be able to read the delivery note.

#### Scenario: Contractor delivers
- **WHEN** the assigned contractor marks an `in_progress` job delivered with note "Module installed on staging"
- **THEN** the job becomes `delivered`, its delivery time is recorded and the customer can read the note

#### Scenario: Unassigned contractor cannot deliver
- **WHEN** a contractor whose proposal on the job was closed attempts to mark it delivered
- **THEN** the request fails exactly as if the job did not exist

### Requirement: Requesting changes
The customer SHALL be able to send a `delivered` job back to `in_progress`, with a required reason. The reason SHALL be readable by the assigned contractor. The job's revision count SHALL increase by one.

#### Scenario: Customer requests changes
- **WHEN** the customer requests changes on a `delivered` job with reason "Report totals are wrong"
- **THEN** the job becomes `in_progress`, its revision count increases by one, and the contractor can read the reason

#### Scenario: Missing reason
- **WHEN** the customer requests changes without a reason
- **THEN** the request is rejected

### Requirement: Completion requires customer confirmation
A job SHALL become `done` only when the customer confirms completion of a `delivered` job, or when a marketplace manager resolves a `delivered` job to `done` through the explicit manager resolution operation with a recorded reason. Completion SHALL record the completion time. In v1 completion SHALL NOT happen automatically: no elapsed time, schedule, inactivity, or background process SHALL move a job to `done`. Manager intervention in a stuck or exceptional delivery SHALL be possible only through the explicit manager operations (resolve to `done`, or cancel), never through generic writes.

#### Scenario: Customer confirms
- **WHEN** the customer confirms completion of a `delivered` job
- **THEN** the job becomes `done` and its completion time is recorded

#### Scenario: Manager resolves an unresponsive customer
- **WHEN** a marketplace manager resolves a `delivered` job to `done` with reason "Customer unresponsive 30 days"
- **THEN** the job becomes `done`, its completion time is recorded, and the reason and manager are recorded in the audit trail

#### Scenario: Delivered job never completes by itself
- **WHEN** a job has been `delivered` for any length of time without customer or manager action
- **THEN** it remains `delivered`, with no completion time and no review eligibility

### Requirement: Cancellation after assignment
A cancellation after assignment SHALL record the cancellation time, the reason, and the cancelling role (`customer`, `contractor`, or `manager`). The accepted proposal SHALL remain `accepted`, as a historical record of the agreed terms. A cancelled job SHALL NOT be eligible for reviews and SHALL NOT count as completed.

Once a job is `delivered`, neither the customer nor the assigned contractor SHALL be able to cancel it. A delivered job SHALL proceed only by:
- customer confirmation;
- a customer change request (which returns it to `in_progress`);
- an explicit manager resolution or manager cancellation with a reason.

#### Scenario: Contractor abandons with reason
- **WHEN** the assigned contractor cancels an `in_progress` job with reason "Unable to access environment"
- **THEN** the job becomes `cancelled` with role `contractor` and the reason recorded, and its accepted proposal stays `accepted`

#### Scenario: Customer cannot cancel after delivery
- **WHEN** the customer attempts to cancel a `delivered` job
- **THEN** the request is rejected and the job stays `delivered`

#### Scenario: Contractor cannot cancel after delivery
- **WHEN** the assigned contractor attempts to cancel a `delivered` job
- **THEN** the request is rejected and the job stays `delivered`

#### Scenario: Cancellation possible again after a change request
- **WHEN** the customer requests changes on a `delivered` job, and the assigned contractor then cancels the now-`in_progress` job with a reason
- **THEN** the job becomes `cancelled` with role `contractor`

### Requirement: Participant-only access during and after execution
While a job is `in_progress`, `delivered`, `done`, or `cancelled`, only the customer, the assigned contractor and marketplace managers SHALL be able to read it. Contractors whose proposals were closed or declined SHALL keep read access to their own proposal only, not to the job's execution details.

#### Scenario: Losing contractor loses job access
- **WHEN** contractor B, whose proposal was closed with `job_filled`, reads the now-`in_progress` job
- **THEN** access is denied, but contractor B can still read their own closed proposal

### Requirement: Execution timestamps for metrics
A job SHALL keep its publication, assignment, latest delivery, completion and cancellation times as they are recorded by the corresponding transitions. These timestamps SHALL NOT be modifiable by any generic write.

#### Scenario: Completion duration is derivable
- **WHEN** a job was assigned on day 1 and confirmed done on day 11
- **THEN** its recorded assignment and completion times allow a completion duration of 10 days to be computed
