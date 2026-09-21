# Tasks

## 1. Project Contract data and lifecycle

- [x] 1.1 Add and test primary Contractor, lifecycle, and compensation amount/currency with safe defaults and one-primary validation.
- [x] 1.2 Add and test minimal candidate membership, or document with tests why an existing native relation is sufficient.
- [x] 1.3 Preserve task contractor history separately from Project primary assignment and test non-conflicting behavior.

## 2. Lifecycle security

- [x] 2.1 Implement and test Discoverable read-only Project/Task access with no private candidate disclosure.
- [x] 2.2 Implement and test Candidate communication-only authority with no Project relationship or Task mutation.
- [x] 2.3 Implement and test Assigned Contractor Project operational writes and Task CRUD limited to their Project.
- [x] 2.4 Implement and test customer/internal-only customer, assignment, reassignment, and closure changes.

## 3. Verification

- [x] 3.1 Run focused lifecycle/security tests after clean install and upgrade on a disposable database: clean install and upgrade of `contractor_lifecycle_clean_20260921` passed all 53 focused lifecycle, access, participation, history, and task-assignment tests.
- [x] 3.2 Run strict OpenSpec validation and `git diff --check`; update tasks only after implementation verification.
