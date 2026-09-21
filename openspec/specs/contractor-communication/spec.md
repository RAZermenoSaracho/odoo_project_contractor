# contractor-communication Specification

## Purpose

Provides private, native-Odoo communication with separate recruitment and
execution boundaries.

## Requirements

### Requirement: Proposal negotiation is private

Each Proposal's recruitment communication SHALL be readable only by the
Proposal's Contractor, users of the Contract customer's commercial entity as
authorized for that Contract, and appropriately authorized internal staff.
Publishing or browsing a Contract SHALL NOT grant access to any Proposal or its
messages, including another Contractor's Proposal.

#### Scenario: Contractor cannot read a competing Proposal

- **WHEN** Contractor A has a Proposal for a published Contract and Contractor B has a different Proposal
- **THEN** A cannot read B's Proposal or B's negotiation messages

### Requirement: Project chatter is operational communication after award

After award, Project chatter SHALL be the operational communication surface for
the customer commercial entity, the Assigned Contractor, and authorized
internal staff. Proposal chatter SHALL remain the private recruitment history
and SHALL NOT be exposed merely because a Project was awarded.

#### Scenario: Award does not reveal competing negotiations

- **WHEN** a customer's Proposal from Contractor A is accepted
- **THEN** the resulting Project does not expose Contractor B's Proposal messages to A

### Requirement: Native communication reuse
The addon SHALL reuse Odoo mail, chatter, followers, project sharing, or Discuss
facilities where they meet the required audience boundary. It SHALL NOT create a
parallel custom messaging subsystem.

#### Scenario: Proposal participant sends a message

- **WHEN** an authorized Proposal participant sends a negotiation message
- **THEN** it is delivered through the selected native Odoo mechanism only to its authorized audience
