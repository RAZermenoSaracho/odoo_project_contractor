# contractor-project-lifecycle Specification

## Purpose

Adds the minimal Project-as-Contract lifecycle separating discovery, candidate
recruitment, and selected Contractor work authority.

## Requirements

### Requirement: One Project Contract has one primary Contractor

A Project/Contract SHALL have zero or one primary Assigned Contractor and MAY
have multiple admitted Candidates. Invitation, contact, or a candidate reply
SHALL NOT assign the primary Contractor.

#### Scenario: Several candidates remain unassigned

- **WHEN** a customer admits two Contractors as candidates
- **THEN** both remain candidates while the primary Contractor is unset

### Requirement: Contractor task authority is lifecycle-specific

A Discoverable Contractor and a Candidate SHALL have no Task create, write, or
delete authority. The Assigned Contractor SHALL have Task create, read, write,
and delete authority only in their assigned Project.

#### Scenario: Assigned Contractor creates a task

- **WHEN** the primary Contractor creates a Task in their assigned Project
- **THEN** creation succeeds

#### Scenario: Candidate cannot edit task

- **WHEN** a candidate modifies a Task in a Project where they are not primary
- **THEN** the operation is denied
