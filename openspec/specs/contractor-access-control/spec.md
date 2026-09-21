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

### Requirement: Contract, Proposal, Project, and Task authority
A Contractor MAY read published Contracts and create or manage only their own
Proposals for those Contracts. A Contractor SHALL not access draft or private
Contracts merely through the Contractor role, nor another Contractor's Proposal.
An Assigned Contractor may operationally write only their awarded execution
Project and create, read, write, and delete Tasks only in that Project. A
Contractor SHALL never obtain access to a Project assigned to another
Contractor, nor browse unassigned Projects as work opportunities.

#### Scenario: Other contractor Project is hidden
- **WHEN** a Contractor searches Projects assigned only to another Contractor
- **THEN** those Projects are absent from the result

#### Scenario: Competing Proposal is hidden
- **WHEN** a Contractor searches Proposals submitted by another Contractor
- **THEN** those Proposals are absent from the result

### Requirement: Contractors cannot alter the commercial relationship
A Contractor SHALL NOT change a Contract customer, publish or close a Contract,
accept or reject another Proposal, assign or reassign a Project Contractor, or
change a Project's commercial relationship. Those operations belong to the
customer commercial entity or appropriately authorized internal staff.

#### Scenario: Contractor attempts reassignment
- **WHEN** an Assigned Contractor attempts to change the Project's customer or Contractor assignment
- **THEN** the operation is denied
