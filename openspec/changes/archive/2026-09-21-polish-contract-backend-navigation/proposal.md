# Proposal

## Why

The Contract and Proposal workflow is available in the backend but lacks its
native navigation surfaces. Staff need concise paths between Contracts,
execution Projects, and a Contractor's awarded work without changing access or
commercial workflow behavior.

## What Changes

- Add the existing Contracts action to the Project application navigation.
- Present a Project's award links and read-only terms in a dedicated Contract
  notebook tab, with a smart button back to its originating Contract.
- Add Contract smart buttons for its Proposals and resulting Project.
- Add a Contractor-contact smart button for Contracts it won, derived solely
  from accepted Proposals.

## Capabilities

### New Capabilities

- `contractor-backend-navigation`: Native backend menus, tabs, and record
  navigation for the existing Contract, Proposal, Project, and Contractor data.

### Modified Capabilities

<!-- None. This change exposes existing relationships without changing their domain behavior or authority. -->

## Impact

Touches only `project_contractor` backend views, small computed/action helpers,
and focused non-browser tests. It adds no dependencies, domain models,
authorization rules, portal routes, or communication behavior.
