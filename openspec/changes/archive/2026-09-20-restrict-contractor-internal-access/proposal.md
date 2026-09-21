# Proposal

## Why

The current addon has a partially implemented Contractor access foundation, but
it is not yet verified as a complete least-privilege role under the clarified
Project/Contract lifecycle.

## What Changes

- Establish and test automatic, identity-preserving Contractor activation.
- Restrict the native Contractor group to the required backend boundary and own partner profile.
- Establish base Project/Task access for assigned and genuinely open work.
- Exclude RPC interception, route allowlists, grant ledgers, attachment layers, and module inventories.

## Capabilities

### New Capabilities
- `contractor-internal-isolation`: Native Contractor activation and base access boundary.

### Modified Capabilities
- `contractor-access-control`: Replace the former no-security foundation with the Contractor role requirements.

## Impact

Touches only `project_contractor` security, user/contact and project/task extensions,
focused ORM tests, and minimal authenticated activation surface.
