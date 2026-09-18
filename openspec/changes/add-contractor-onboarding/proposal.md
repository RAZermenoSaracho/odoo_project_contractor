## Why

Contact classification and marketplace publication do not implement administrator-reviewed internal access. Contractors need an auditable application and a safe transition of their existing portal identity.

## What Changes

- Add private applications with submit, withdraw, reject, approve and revoke operations.
- Restrict internal approval to settings administrators after the isolation layer verifies the resulting effective access; approval grants zero workspaces.
- Keep customer opportunity creation independent of contractor status, and public profile publication distinct from account approval.

## Capabilities

### New Capabilities
- `contractor-onboarding`: Application review and atomic, reversible portal-to-restricted-internal transitions.

### Modified Capabilities
None.

## Impact

New sibling addon `project_contractor_onboarding`, depending on `project_contractor_access`; backend review views and operations. Portal application pages belong to `add-contractor-portal-workflow`. No marketplace dependency or duplicated profile identity.

Planning only. These decisions are proposed for review; implementation and archiving require separate explicit approval.
