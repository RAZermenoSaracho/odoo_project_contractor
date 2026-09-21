# Proposal

## Why

The current Project-as-opportunity design conflates public recruitment, private
negotiation, and awarded execution. Separate Contract and Proposal records give
each relationship its own small lifecycle and privacy boundary while preserving
Project as the workspace where work is actually performed.

## What Changes

- Add small `contract.contract` customer opportunities and `contract.proposal`
  one-Contractor negotiations.
- Add Contract publication and award behavior, Proposal terms/state transitions,
  and atomic, idempotent acceptance that creates one linked execution Project.
- **BREAKING** Move Contractor opportunity discovery and recruitment away from
  `project.project`: Contractors browse published Contracts, access only their
  own Proposals, and see only Projects to which they are assigned.
- **BREAKING** Retire Project candidate recruitment, unassigned Project
  discovery, and competing Project compensation fields/rules; preserve awarded
  Project operational restrictions and Task CRUD for its Assigned Contractor.
- Migrate compatible existing assigned Projects to an awarded Contract/Proposal
  linkage without fabricating candidate negotiations; leave unrelated ordinary
  Projects intact.

## Capabilities

### New Capabilities

- `contractor-contract-proposal-workflow`: Customer-owned Contracts, private
  Contractor Proposals, award transitions, and Project creation.

### Modified Capabilities

- `contractor-access-control`: Move Contractor recruitment access from Projects
  to published Contracts and own Proposals, while retaining assigned execution access.
- `contractor-project-workflow`: Define Project as the one execution workspace
  created from an accepted Proposal.
- `contractor-project-lifecycle`: Replace Project discovery/candidate authority
  with Assigned-Contractor-only execution authority.
- `contractor-project-participation`: Separate task-derived history from the
  accepted-Proposal execution assignment rather than Project candidate membership.
- `contractor-addon-distribution`: Include the generic Contract/Proposal domain
  in the portable single-addon workflow.

## Impact

Touches `project_contractor` models, native ACLs and record rules, Project
extensions and migration, backend views, focused ORM/security tests, and later
portal/communication changes. It uses Odoo partner, currency, mail, Project,
and portal mechanisms; it adds no marketplace, payment, or custom authorization
framework.
