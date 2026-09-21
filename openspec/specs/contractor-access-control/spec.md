# contractor-access-control Specification

## Purpose

Defines the restricted internal Contractor role and its least-privilege access to
the Contractor workflow without creating a parallel authorization system.

## Requirements

### Requirement: Automatic identity-preserving activation
An authenticated portal user SHALL be able to explicitly activate Contractor
access for their existing user and partner identity. Activation SHALL require no
administrator approval and SHALL NOT create a second user or contact.

#### Scenario: Portal user becomes a Contractor
- **WHEN** an authenticated portal user selects "Become a Contractor"
- **THEN** that same user becomes an internal Contractor and retains the same partner

### Requirement: Contractor backend boundary
A Contractor SHALL receive only the normal internal access needed for Projects,
Tasks, their own profile, and required communication. The addon SHALL NOT grant
unrelated business-application access merely because the user is a Contractor.

#### Scenario: Unrelated records remain inaccessible
- **WHEN** a Contractor attempts to open an unrelated internal application record
- **THEN** normal Odoo access control denies it unless another authorized group grants it

### Requirement: Contractor profile access
A Contractor SHALL read and write their own partner record as needed by the
workflow and SHALL NOT create, read, write, or delete arbitrary contacts through
the Contractor role.

#### Scenario: Foreign contact is denied
- **WHEN** a Contractor attempts to read or edit another partner record
- **THEN** access is denied

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

### Requirement: Contractors cannot alter the commercial relationship
A Contractor SHALL NOT assign or reassign the primary Contractor, change the
customer, or close a Project/Contract. Those operations belong to the customer
or appropriately authorized internal staff.

#### Scenario: Contractor attempts reassignment
- **WHEN** an Assigned Contractor attempts to change the Project's customer or primary Contractor
- **THEN** the operation is denied
