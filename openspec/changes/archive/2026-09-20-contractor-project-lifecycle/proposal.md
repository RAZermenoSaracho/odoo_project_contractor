# Proposal

## Why

The foundation classifies task contractors but does not model the one
Project-as-Contract lifecycle that separates public discovery, private
recruitment, and operational work.

## What Changes

- Represent open, candidate, assigned, and closed workflow using a primary
  Contractor, minimal compensation amount/currency, and minimal participation.
- Permit multiple candidates but exactly one primary Assigned Contractor in v1.
- Give an Assigned Contractor Project operational write access and full Task
  CRUD; Discoverable and Candidate Contractors remain read-only outside communication.

## Capabilities

### New Capabilities
- `contractor-project-lifecycle`: Project-as-Contract lifecycle and authority.

### Modified Capabilities
- `contractor-access-control`: Make Project and Task permissions lifecycle-specific.
- `contractor-project-participation`: Separate historical task participation from recruitment and assignment.

## Impact

Touches Project/Task models, native ACLs/record rules, views, upgrades, and focused lifecycle tests.
