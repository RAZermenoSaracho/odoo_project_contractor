## Why

The repository has inherited backend views only, and the domain marketplace deliberately provides no frontend. The complete product needs reusable portal navigation and pages for customers and contractors.

## What Changes

- Add registration/login handoff, application status, directory, opportunity creation/uploads, private outreach and negotiation pages.
- Add explicit authorize-work confirmation, active contracts, workspace execution pages and safe error/empty states.
- Provide a single installable workflow frontend with backend navigation for approved contractors and reviewers, and complete multi-user browser acceptance tests.

## Capabilities

### New Capabilities
- `contractor-portal-workflow`: End-to-end portal/backend navigation with authorization-preserving controllers and installation contract.

### Modified Capabilities
None.

## Impact

New sibling addon `project_contractor_portal`, depending on `project_contractor_workflow`, `portal`, and `auth_signup`; use native portal layouts without requiring `website` unless a reviewed implementation need is established. Depends on all required domain/security changes, not on optional reputation. No tenant, hosting or SSO integration.

Planning only. These decisions are proposed for review; implementation and archiving require separate explicit approval.
