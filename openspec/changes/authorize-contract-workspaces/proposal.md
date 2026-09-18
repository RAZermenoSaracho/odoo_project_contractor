## Why

Accepting a marketplace offer is not currently linked to protected Project resources, and contractor assignment is only classification. Customer authorization must create precisely scoped effective work access and an active-contract workflow.

## What Changes

- Bind the customer decision to exact offer revision, agreed terms and explicit work authorization in one atomic operation.
- Create a dedicated protected Project workspace for each authorized contract and grant access only to its enumerated resources.
- Require administrator-approved restricted internal status for work access; implement revocation, terminal-state access policy and active contracts.

## Capabilities

### New Capabilities
- `contract-workspace-authorization`: Customer-controlled authorization, scoped Project work, revocation and active-contract membership.

### Modified Capabilities
None.

## Impact

New sibling addon `project_contractor_workflow`, depending on `project_contractor_onboarding` and `project_contractor_negotiation`. Requires isolation, onboarding and marketplace/negotiation first, and foundation history regression fixes before integrated verification. Adds optional integration to the core marketplace acceptance operation; all alternate entry points must enforce the same authorization checks.

Planning only. These decisions are proposed for review; implementation and archiving require separate explicit approval.
