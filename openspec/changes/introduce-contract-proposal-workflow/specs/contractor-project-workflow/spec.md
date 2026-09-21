# Spec Delta

## MODIFIED Requirements

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
