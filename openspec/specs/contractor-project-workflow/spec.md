# contractor-project-workflow Specification

## Purpose

Uses one `project.project` as the customer-to-Contractor contract and workspace,
with a small, explicit recruitment and assignment lifecycle.

## Requirements

### Requirement: Project is the Contract
A customer-facing Project SHALL be the Contract/workspace in v1. The addon
SHALL NOT create a separate contract, proposal, bidding, invoice, or payment
domain merely to represent the workflow.

#### Scenario: Customer creates a contract
- **WHEN** a customer creates a Contract through the workflow
- **THEN** the system creates a Project owned by that customer's partner relationship

### Requirement: Customer ownership follows the commercial entity
For customer portal ownership, a Project's `partner_id` SHALL identify the
customer contact relationship. An authenticated portal user SHALL be a customer
owner when that user's `partner_id.commercial_partner_id` equals the Project
customer's `partner_id.commercial_partner_id`. The rule SHALL include the
customer's normal parent/child contacts under that one commercial entity and
SHALL NOT grant access to a different commercial entity merely because it is a
contact, follower, candidate, collaborator, or Contractor.

#### Scenario: Colleague manages a company Contract
- **WHEN** a Project customer is a contact of Acme and another portal user is a
  contact of Acme with the same commercial partner
- **THEN** that user can access and manage the Project as its customer

#### Scenario: Unrelated contact is denied
- **WHEN** a portal user belongs to a commercial entity different from the
  Project customer's commercial partner
- **THEN** that user cannot access or manage the Project through customer ownership

### Requirement: One primary Contractor and multiple candidates
A Project/Contract SHALL have at most one primary Assigned Contractor in v1 and
MAY have multiple Participants/Candidates during recruitment. Inviting or
contacting a Contractor SHALL NOT make that Contractor the primary assignment.

#### Scenario: Invitation does not assign
- **WHEN** a customer invites a Contractor to a Project
- **THEN** the Contractor is a Participant/Candidate and the primary Contractor remains unset

### Requirement: Minimal compensation terms
A Project/Contract SHALL represent an agreed or proposed compensation amount and
currency. Discussion of terms SHALL use the workflow communication; v1 SHALL
NOT implement invoicing, escrow, milestones, or payment processing.

#### Scenario: Compensation is recorded
- **WHEN** a customer records a proposed amount and currency
- **THEN** the Project retains those structured values without creating an invoice or payment

### Requirement: Lifecycle authority
A Project/Contract SHALL distinguish Discoverable, Participant/Candidate, and
Assigned Contractor authority. Discoverable work has no primary Contractor;
Participant/Candidate admission is private recruitment access; Assigned
Contractor grants operational work authority.

#### Scenario: Candidate is not operationally assigned
- **WHEN** a candidate has not been selected as the primary Contractor
- **THEN** that candidate cannot perform Assigned Contractor project or task operations
