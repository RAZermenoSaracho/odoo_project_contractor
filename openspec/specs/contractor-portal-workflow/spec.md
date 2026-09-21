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
