# Spec Delta

## ADDED Requirements

### Requirement: Contract is a customer-owned published opportunity

The addon SHALL provide `contract.contract` as a small customer-owned work
opportunity with `draft`, `published`, `awarded`, and `cancelled` states. Its
customer is `partner_id`; customer portal authority SHALL require equality of
the requester's and Contract customer's `commercial_partner_id`. Contractors
may read only published Contracts and SHALL not create, modify, delete, or read
private Contract records through their Contractor role.

#### Scenario: Published Contract is visible to Contractor

- **WHEN** a customer publishes a Contract
- **THEN** a Contractor may read its permitted opportunity projection but cannot modify it

### Requirement: Proposal is one Contractor's private negotiation

The addon SHALL provide `contract.proposal` linked to exactly one Contract and
one Contractor, with amount, currency, and states `draft`, `submitted`,
`accepted`, `rejected`, and `withdrawn`. A Contractor may create a Proposal for
a published Contract and manage only their own Proposal. A customer invitation
MAY initialize that Contractor's draft Proposal and SHALL NOT create a separate
invitation domain object.

#### Scenario: Contractor cannot read competing Proposal

- **WHEN** two Contractors submit Proposals for one Contract
- **THEN** each Contractor can access only their own Proposal

### Requirement: Proposal acceptance awards one Project

Accepting a submitted Proposal SHALL atomically set it as the Contract's one
accepted Proposal, transition competing active Proposals consistently, mark the
Contract awarded, and create or retain exactly one linked execution Project. The
accepted Proposal is authoritative for amount and currency, and the accepted
Contractor becomes the Project's Assigned Contractor.

#### Scenario: Acceptance retry is idempotent

- **WHEN** an authorized customer retries acceptance of an already accepted Proposal
- **THEN** no duplicate Project is created and the original linkage remains
