# contractor-private-communication Specification

## Purpose

Defines exact private recruitment and post-award communication audiences using
native Odoo communication facilities and existing record authorization.

## Requirements

### Requirement: Recruitment communication has an exact audience
Each Proposal recruitment conversation SHALL be limited to its Contract's
authorized customer commercial entity, that Proposal's Contractor, and
authorized internal staff. Contractors browsing a published Contract SHALL not
become members solely by viewing it.

#### Scenario: Contract browser is not a member
- **WHEN** a Contractor reads a published Contract without their own Proposal
- **THEN** that Contractor cannot read another Proposal's recruitment conversation

### Requirement: Native conversation membership is revocable
Withdrawing, rejecting, or awarding a Proposal SHALL preserve its required
history without granting another Contractor access to that Proposal's private
recruitment conversation through the native mechanism.

#### Scenario: Competing Proposal remains private after award
- **WHEN** a customer accepts one Proposal
- **THEN** the accepted Contractor cannot retrieve a competing Proposal's conversation

### Requirement: Project communication is post-award operational communication
The Project's native operational conversation SHALL be limited to the customer
commercial entity, the Assigned Contractor, and authorized internal staff. It
SHALL NOT expose Proposal negotiation history.

#### Scenario: Project does not expose Proposal history
- **WHEN** an accepted Proposal creates a Project
- **THEN** Project participants cannot retrieve unrelated Proposal messages
