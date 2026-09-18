## Why

The implemented foundation records outside contractors but has no customer opportunities, offers or commercial lifecycle. A reusable, presentation-independent marketplace core supplies those primitives without pretending commercial assignment grants protected database access.

## What Changes

- Add optional sibling addon `project_contractor_marketplace`, depending exactly on `project_contractor`.
- Add public profile projections, generic skills, customer opportunity listings, private proposals, customer-only atomic acceptance and delivery/completion operations.
- Keep exact-partner ownership, ORM/RPC-safe operations, company scope, field privacy, durable manager-only audit and closed core chatter/attachments.
- Distinguish self-publication from administrator-approved internal status and customer-authorized work. Standalone core creates no Project workspace or access grants.
- Define extension contracts for revision-aware negotiation and authorization within the same acceptance transaction; the full product uses those extensions and shipped portal pages.
- Split unimplemented reviews and reputation into `add-marketplace-reviews-reputation`; no work is represented as complete by that move.

## Capabilities

### New Capabilities
- `marketplace-contractor-profiles`: public projection, self-publication and suspension, separate from account approval.
- `marketplace-jobs`: customer-owned opportunity listings, currency, publication and edit locks.
- `marketplace-proposals`: private structured offers and lifecycle.
- `marketplace-assignment`: customer-only atomic commercial acceptance and extension preconditions.
- `marketplace-job-execution`: delivery, changes, confirmation and cancellation with effective-authorization extension checks.
- `marketplace-access-control`: actors, company-scoped record access, protected fields and closed core audit channels.
- `marketplace-domain-api`: caller-derived allowlisted operations, dependencies and integration contracts.
- `marketplace-audit-trail`: server timestamps, real actors, reasons and manager-only durable history.

### Modified Capabilities
None. The six foundation capabilities already exist in `openspec/specs/`; the foundation was archived on 2026-09-14. This change adds an optional layer and preserves the foundation installed alone.

## Impact

Proposed sibling addon in this repository under LGPL-3, matching the existing approved foundation license. No addon code exists yet; all implementation tasks remain pending. The complete product also needs isolation, onboarding, private negotiation/documents, authorized workspaces and portal delivery, tracked as separate changes. Sales, payments, hosting, tenant/SSO integration and optional reputation are not core prerequisites.

This revision replaces stale 2026-09-14 scope assumptions with the 2026-09-18 product intent. Self-publication remains separate from internal approval; blanket bans on all future messaging/uploads are replaced by closed core audit records plus explicitly scoped extensions. Planning only; await review and explicit apply authorization.
