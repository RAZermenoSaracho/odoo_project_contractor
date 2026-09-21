# Spec Delta

## Purpose

Adds minimal generic portal journeys so customers can publish Contracts, review
Proposals, and award Projects while Contractors can propose, communicate, and
perform authorized work.

## ADDED Requirements

### Requirement: Customer can create, publish, and award through the portal
An authenticated customer SHALL be able to create a Contract they own, publish
it, browse publishable Contractor profiles, invite/contact a Contractor by
initializing a Proposal where appropriate, review Proposals, and accept one.
The invitation operation SHALL not assign the Contractor or create a Project.

#### Scenario: Customer starts recruitment
- **WHEN** a customer creates a Contract and invites a directory Contractor
- **THEN** the Contract belongs to that customer and the Contractor has at most their own draft Proposal, not an assigned Project

### Requirement: Customer ownership is commercial-entity scoped
Customer management access SHALL include portal users whose partner has the same
`commercial_partner_id` as the Contract customer's `partner_id`. It SHALL not
include a portal user from another commercial entity unless another explicit
workflow authorization applies.

#### Scenario: Same commercial entity manages a Contract
- **WHEN** the Contract customer and a portal user's partner share a commercial partner
- **THEN** that user can manage the Contract through the customer workflow

#### Scenario: Different commercial entity cannot manage
- **WHEN** a portal user's partner has a different commercial partner from the Project customer
- **THEN** customer management access is denied

### Requirement: Contractor portal distinguishes proposal and execution authority
An activated Contractor SHALL see published Contracts, only their own Proposals,
and only their assigned Projects through separate workflow entries. Contract
entries SHALL not show private competing negotiation; Proposal entries SHALL
not expose Project Task operations; assigned Project entries SHALL provide
Project/Task work navigation.

#### Scenario: Proposal landing page
- **WHEN** a Contractor opens their Proposal workflow page
- **THEN** they can enter only their authorized negotiation and cannot create or edit Project Tasks before award
