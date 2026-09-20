# contractor-portal-workflow Specification

## Purpose

Defines the minimal generic portal and website journeys for customers and
Contractors to complete the Project/Contract workflow.

## Requirements

### Requirement: Customer portal workflow
An authenticated portal customer SHALL be able to create a Project/Contract,
view and manage Projects owned by their commercial entity or in which they
otherwise participate, browse available Contractor
profiles, and invite/contact a Contractor for a specific Project.

#### Scenario: Customer invites a Contractor
- **WHEN** a customer selects a Contractor from the generic directory for one of their Projects
- **THEN** the Contractor becomes a private Participant/Candidate, not the Assigned Contractor

#### Scenario: Commercial-entity customer access
- **WHEN** two portal users belong to the Project customer's same commercial entity
- **THEN** either can use the customer workflow for that Project

### Requirement: Contractor portal workflow
An authenticated portal user SHALL be able to activate Contractor access, edit
their permitted profile, browse discoverable opportunities, see Projects where
they are a Participant or Assigned Contractor, and enter only communication or
work pages authorized for their lifecycle state.

#### Scenario: Contractor sees authorized opportunities
- **WHEN** a Contractor opens their workflow landing page
- **THEN** it distinguishes discoverable, candidate, and assigned Projects without disclosing private candidate data for discoverable work

### Requirement: Minimal reusable presentation
The module SHALL supply functional, intentionally minimal QWeb portal/website
pages and navigation. Branding, copy, layout, and styling specific to another
site SHALL remain outside the module.

#### Scenario: Generic page has no RAZS dependency
- **WHEN** a clean database renders a Contractor workflow page
- **THEN** it does not require RAZS templates, assets, or branding
