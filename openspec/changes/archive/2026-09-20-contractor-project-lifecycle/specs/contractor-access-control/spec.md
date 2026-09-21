# Spec Delta

## MODIFIED Requirements

### Requirement: Project and task access follows lifecycle authority
Contractor access to a Project and its Tasks SHALL follow the current Contractor
relationship to that Project: Discoverable, Participant/Candidate, or Assigned
Contractor. A Discoverable Contractor may read only permitted opportunity
information and existing Tasks; a Participant/Candidate may use authorized
private communication but may not mutate the Project or Tasks; an Assigned
Contractor may operationally write their Project but may not alter customer,
primary assignment, reassignment, or closure, and may create, read, write, and
delete Tasks only in that Project. A Contractor SHALL never obtain access to a
Project assigned solely to another Contractor.

#### Scenario: Other contractor project is hidden
- **WHEN** a Contractor searches Projects assigned only to another Contractor
- **THEN** those Projects are absent from the result

#### Scenario: Open opportunity is read-only
- **WHEN** a Contractor opens a Discoverable Project
- **THEN** they can read permitted information but cannot mutate the Project or its Tasks
