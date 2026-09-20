# Spec Delta

## Purpose

Adds minimal generic portal journeys so customers can recruit Contractors and
Contractors can discover, communicate about, and perform authorized work.

## ADDED Requirements

### Requirement: Customer can create and recruit through the portal
An authenticated customer SHALL be able to create a Project/Contract they own,
browse publishable Contractor profiles, and invite/contact a Contractor for that
Project. The invite operation SHALL not assign the Contractor.

#### Scenario: Customer starts recruitment
- **WHEN** a customer creates a Project and invites a directory Contractor
- **THEN** the Project belongs to that customer and the Contractor is a candidate, not assigned

### Requirement: Customer ownership is commercial-entity scoped
Customer management access SHALL include portal users whose partner has the same
`commercial_partner_id` as the Project customer's `partner_id`. It SHALL not
include a portal user from another commercial entity unless another explicit
workflow authorization applies.

#### Scenario: Same commercial entity manages a Project
- **WHEN** the Project customer and a portal user's partner share a commercial partner
- **THEN** that user can manage the Project through the customer workflow

#### Scenario: Different commercial entity cannot manage
- **WHEN** a portal user's partner has a different commercial partner from the Project customer
- **THEN** customer management access is denied

### Requirement: Contractor portal distinguishes authority states
An activated Contractor SHALL see Discoverable, Candidate, and Assigned Projects
through separate workflow entries. Discoverable entries SHALL not show private
negotiation; Candidate entries SHALL not expose task operations; Assigned entries
SHALL provide Project/Task work navigation.

#### Scenario: Candidate landing page
- **WHEN** a candidate opens their Contractor workflow page
- **THEN** they can enter authorized communication but cannot create or edit Project Tasks
