# Spec Delta

## MODIFIED Requirements

### Requirement: Contract, Proposal, Project, and Task authority

A Contractor MAY read published Contracts and create or manage only their own
Proposals for those Contracts. A Contractor SHALL not access draft or private
Contracts merely through the Contractor role, nor another Contractor's Proposal.
An Assigned Contractor may operationally write only their awarded execution
Project and create, read, write, and delete Tasks only in that Project. A
Contractor SHALL never obtain access to a Project assigned to another Contractor
or browse unassigned Projects as opportunities.

#### Scenario: Other contractor Project is hidden

- **WHEN** a Contractor searches Projects assigned only to another Contractor
- **THEN** those Projects are absent from the result

#### Scenario: Competing Proposal is hidden

- **WHEN** a Contractor searches Proposals submitted by another Contractor
- **THEN** those Proposals are absent from the result
