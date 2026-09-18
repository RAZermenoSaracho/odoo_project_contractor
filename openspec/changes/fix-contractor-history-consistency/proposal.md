## Why

The foundation history implementation is broadly present, but the raw task relation does not match the specified company roll-up/exclusions, and counts have no task dependency declarations. Existing refresh tests explicitly invalidate the environment, leaving an important observable refresh guarantee unproven.

## What Changes

- Make direct history reads, counts, searches and navigation use the same excluded-task and company roll-up semantics.
- Require same-transaction refresh after changes without caller cache invalidation, while retaining per-viewer access filtering.
- Close the evidence gap with targeted regression tests and recorded disposable-database verification when apply is authorized.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `contractor-work-history`: Clarify consistent relation, count and navigation semantics and immediate refresh.
- `contractor-project-participation`: Require navigation/count agreement and same-transaction refresh.

## Impact

Existing `project_contractor/models/res_partner.py`, `project_project.py`, task invalidation/dependencies as needed, and their tests. No new access grant, identity, dependency or lifecycle. Independent maintenance; preserve archived history.

Planning only. These decisions are proposed for review; implementation and archiving require separate explicit approval.
