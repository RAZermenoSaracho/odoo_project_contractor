## Why

Ordinary internal users inherit broad database access; the current foundation intentionally does not narrow it. A verified restriction layer must exist before any contractor is promoted from portal to internal.

## What Changes

- Add a separately installable, default-deny restricted internal role with explicit per-record grants and a reviewed model/operation access inventory.
- Prevent implied groups, company membership, followers, generic RPC and attachments from widening contractor access; fail closed for unsupported installed modules.
- Preserve ordinary employee behavior and the standalone foundation. This layer exposes no self-service promotion or customer authorization endpoint.

## Capabilities

### New Capabilities
- `contractor-internal-isolation`: Database-wide boundary for restricted internal accounts, effective grants, revocation and compatible installations.

### Modified Capabilities
None.

## Impact

New sibling addon `project_contractor_access`, depending on `project_contractor`, under LGPL-3 as a proposed packaging choice. Touches user/group transitions, ACL/rule integration and record access in a later apply only. Independent of marketplace. Onboarding depends on its verified boundary.

Planning only. These decisions are proposed for review; implementation and archiving require separate explicit approval.
