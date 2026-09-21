# contractor-contract-proposal-workflow Specification

## Purpose

Defines the customer opportunity and private Contractor negotiation domain that
precedes the awarded Project execution workspace.

## Requirements

### Requirement: Contract is a customer-owned opportunity

`contract.contract` SHALL be the small customer-created work opportunity. Its
customer relationship SHALL use `partner_id`, and customer ownership SHALL be
granted only when the requesting portal user's
`partner_id.commercial_partner_id` equals the Contract customer's
`partner_id.commercial_partner_id`. The Contract lifecycle SHALL be `draft`,
`published`, `awarded`, and `cancelled`; only `published` Contracts are
Contractor-browsable.

#### Scenario: Same commercial entity manages Contract

- **WHEN** a Contract customer and a portal user have the same commercial partner
- **THEN** that portal user may manage the Contract as its customer

#### Scenario: Contractor cannot browse draft Contract

- **WHEN** a Contractor searches Contracts that are still draft
- **THEN** those Contracts are absent unless the user is an authorized customer or internal staff member

### Requirement: Proposal represents one private negotiation

`contract.proposal` SHALL link exactly one Contract and one Contractor. Its
lifecycle SHALL be `draft`, `submitted`, `accepted`, `rejected`, or
`withdrawn`, and it SHALL record amount and currency. A Contractor may create a
Proposal only for a published Contract and may manage only their own Proposal.
A customer invitation MAY create or initialize that Contractor's draft Proposal;
it SHALL NOT require a separate invitation subsystem.

#### Scenario: Contractor submits own Proposal

- **WHEN** a Contractor creates and submits a Proposal for a published Contract
- **THEN** the Proposal belongs only to that Contractor and records its amount and currency

### Requirement: Customer accepts exactly one Proposal

An authorized customer or internal staff member SHALL be able to accept one
submitted Proposal for their Contract. Acceptance SHALL set the Contract's
accepted Proposal, mark the Contract awarded, transition competing active
Proposals consistently to rejected, and preserve submitted negotiation history.
Draft Proposals MAY be deleted; submitted Proposals SHALL normally transition
instead of being destructively removed.

#### Scenario: Competing Proposal is rejected on award

- **WHEN** a customer accepts Contractor A's submitted Proposal while Contractor B's Proposal is submitted
- **THEN** A's Proposal is accepted and B's Proposal is rejected

### Requirement: Acceptance is atomic and idempotent

Proposal acceptance SHALL atomically award the Contract and create or retain one
linked execution Project. The accepted Proposal is the authoritative source for
the agreed amount and currency. The transition SHALL be safe to retry and SHALL
not create a second Project.

#### Scenario: Repeated acceptance creates no duplicate Project

- **WHEN** the customer retries acceptance after the first transition completed
- **THEN** the same Contract, accepted Proposal, and Project linkage are returned

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
