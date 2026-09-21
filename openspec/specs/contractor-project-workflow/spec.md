# contractor-project-workflow Specification

## Purpose

Defines `project.project` as the execution workspace created by an accepted
Contract Proposal, rather than as a recruitment opportunity.

## Requirements

### Requirement: Award creates one linked execution Project

Accepting a Contract Proposal SHALL create exactly one execution Project linked
to its Contract and accepted Proposal. Retrying or concurrently invoking the
acceptance transition SHALL return or preserve that one Project and SHALL NOT
create a duplicate award or execution workspace.

#### Scenario: Acceptance is retried

- **WHEN** a customer repeats acceptance of the same accepted Proposal
- **THEN** the Contract retains one accepted Proposal and one linked Project

### Requirement: Project assignment derives from the accepted Proposal

The accepted Proposal's Contractor SHALL be the execution Project's one
Assigned Contractor. Project candidate memberships, unassigned-Project
Contractor discovery, and Project-based recruitment SHALL NOT be used in the
target workflow.

#### Scenario: Awarded Contractor opens the Project

- **WHEN** a Proposal is accepted for Contractor A
- **THEN** the linked Project is assigned to A and Contractor B cannot access it through the Contractor role

### Requirement: Project preserves execution boundaries

An Assigned Contractor MAY make the defined operational Project updates and
manage Tasks in that Project. They SHALL NOT change the Project customer,
Contract/Proposal linkage, assigned Contractor, award terms, or closure state.
Customer commercial ownership and authorized internal staff retain those
commercial operations.

#### Scenario: Assigned Contractor cannot change award relationship

- **WHEN** the Assigned Contractor writes a protected customer, assignment, or linkage field
- **THEN** the operation is denied

### Requirement: Accepted Proposal is commercial source of truth

The accepted Proposal SHALL remain the authoritative amount and currency for
the award. A Project MAY expose a read-only related display where useful, but
SHALL NOT maintain an independently editable competing commercial record.

#### Scenario: Operational Project displays agreed terms

- **WHEN** an authorized user views the awarded Project
- **THEN** any displayed agreed amount and currency correspond to its accepted Proposal
