# contractor-backend-navigation Specification

## Purpose
Defines the compact backend navigation that makes the existing Contract award
relationships discoverable without altering Contract, Proposal, or Project authority.

## Requirements

### Requirement: Contracts are available in Project backend navigation

The Project application SHALL expose a Contracts menu using the existing
Contract list/form action. Menu visibility SHALL not grant any additional model
access; normal ACL and record-rule evaluation SHALL determine readable records.

#### Scenario: Authorized user opens Contracts

- **WHEN** an authorized backend user selects Contracts from Project navigation
- **THEN** the existing Contract list opens and only readable Contracts appear

### Requirement: Award links have native record navigation

An execution Project SHALL present its Contract, accepted Proposal, Assigned
Contractor, and read-only agreed terms in a dedicated Contract tab. A Project
with an originating Contract SHALL provide a smart button to that exact Contract.
A Contract SHALL provide smart buttons to its own Proposals and, when present,
its resulting execution Project.

#### Scenario: Linked Project opens its originating Contract

- **WHEN** a user opens the Contract smart button on a Project linked to Contract C
- **THEN** the action opens only C

#### Scenario: Contract opens only its own Proposals and Project

- **WHEN** a user uses Contract C's Proposals or Project smart button
- **THEN** each action is scoped to C's Proposal records or its one resulting Project respectively

### Requirement: Contractor contact shows won Contracts only

A Contractor contact SHALL display a Contracts count and navigation derived from
Contracts whose accepted Proposal has that Contractor. The count and action
domain SHALL match, and SHALL exclude unaccepted, competing, or unrelated
Proposals and Contracts.

#### Scenario: Contractor opens won Contracts

- **WHEN** Contractor A has an accepted Proposal for Contract C and only an unaccepted or losing Proposal for Contract D
- **THEN** A's Contracts count and action contain C and exclude D
