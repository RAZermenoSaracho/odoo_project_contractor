## Context

The existing `is_contractor` flag neither creates users nor grants access. The proposed marketplace profile is a public projection with self-publication, not an internal-user approval record. See proposal.md and `restrict-contractor-internal-access`.

## Goals / Non-Goals

**Goals:** private auditable applications, safe account transition, revocation and identity continuity.
**Non-Goals:** contractor verification as a customer prerequisite, auto-publication, customer contract grants, changes to native signup policy.

## Decisions

Use sibling `project_contractor_onboarding` depending on `project_contractor_access`, with a small `contractor.application` model keyed to the existing user and partner. A partial unique constraint prevents multiple pending applications. Draft → pending → approved/rejected; pending → withdrawn; approved → revoked. Resubmission creates a fresh application so prior decisions remain durable. Applicant fields are introduction/requested scope only; administrators' notes are separate from applicant-visible reasons.

Only `base.group_system` administrators can approve/reject/revoke. Marketplace managers are not account administrators. Public domain operations derive the caller and reject supplied ownership/status/group fields; generic writes cannot drive decisions. Lock user then application, recheck current state and isolation compatibility, and commit group/type/restriction changes with the decision. The isolation addon owns the private account-transition API and cache invalidation. Remove portal membership and add only the reviewed restricted internal group set atomically, preserving uid/partner. Revocation does the reverse for workflow-managed accounts and disables effective grants before returning.

Reject approval for existing ordinary employees with conflicting roles; do not silently downgrade unrelated staff. Reapproval never restores revoked grants. Record real administrator, server time and reason. Application read rules use exact user ownership, never `commercial_partner_id` roll-up. Backend views are admin-only and show approval status separately from the contractor classification flag.

Self-service public profile activation remains a portal marketplace permission. Work authorization later requires both an active profile and approved restricted account. The full product may therefore list a portal contractor who is still awaiting approval; the portal must show the work-approval prerequisite before authorization, without publishing private application contents.

## Risks / Trade-offs

- [Risk] Concurrent approval/revocation or stale group caches. → Consistent user-first lock ordering, transactional updates and tests through an already authenticated session.
- [Risk] Arbitrary application text exposes personal data. → Applicant/admin-only records, no automatic public profile copy, explicit safe field projection.

## Migration Plan

No inferred approval for flagged contacts or existing internal users. Install only after isolation tests pass. Existing users opt in by application; keep history on revocation. Removing the addon must not remove restrictions while accounts remain internal; use the isolation layer's demotion guard.
