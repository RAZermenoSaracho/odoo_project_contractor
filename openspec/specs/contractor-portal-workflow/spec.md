# contractor-portal-workflow Specification

## Purpose

Defines the minimal generic portal and website journeys for customers and
Contractors through Contract, Proposal, and Project execution.

## Requirements

### Requirement: Customer Contract workflow
An authenticated portal customer SHALL be able to create, manage, and publish
Contracts owned by their commercial entity; review their Contracts' individual
Proposals; communicate in each authorized Proposal; and accept one Proposal.

#### Scenario: Customer reviews independent Proposals
- **WHEN** two Contractors submit Proposals for one published Contract
- **THEN** the customer can review each private Proposal without exposing either one to the competing Contractor

### Requirement: Contractor workflow
An authenticated portal user SHALL be able to activate Contractor access, edit
their permitted profile, browse published Contracts, create and manage only
their Proposals, and work in Projects to which they are assigned.

#### Scenario: Contractor sees only award work
- **WHEN** a Contractor opens their workflow landing page after another Contractor is awarded
- **THEN** they can still browse eligible published Contracts but cannot open the other Contractor's Project

### Requirement: Minimal reusable presentation
The module SHALL supply functional, intentionally minimal QWeb portal/website
pages and navigation. Branding, copy, layout, and styling specific to another
site SHALL remain outside the module.

#### Scenario: Generic page has no RAZS dependency
- **WHEN** a clean database renders a Contractor workflow page
- **THEN** it does not require RAZS templates, assets, or branding

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
