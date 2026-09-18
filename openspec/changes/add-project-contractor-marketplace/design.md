## Context

See proposal.md. Only the foundation exists: contact classification, task contractor, computed participation/history and inherited backend views. The original 2026-09-14 marketplace plan had 45 unchecked tasks and ten capabilities; the 2026-09-18 audit separated optional reviews/reputation and planned the missing workflow. No implementation or archive is claimed.

## Goals / Non-Goals

**Goals:** independently installable domain core; exact-partner ownership; invariant enforcement for ORM/RPC; privacy and concurrency; explicit integration contracts.
**Non-Goals:** internal account approval, Project access grants, participant messaging/file storage, frontend pages, reviews/reputation, sales, payments or deployment topology checks. Those required for the complete workflow are assigned to named changes in `openspec/AUDIT.md`, not deferred indefinitely.

## Decisions

### D1. Native mechanisms with a small domain model

Use sibling `project_contractor_marketplace`, `depends` exactly `project_contractor`, LGPL-3. Models: `contractor.marketplace.profile`, `.skill`, `.job`, `.proposal`, protected-operation mixin and reason wizard. Public profile fields must not live on `res.partner`: readable Many2one names and generic partner reads can expose private contact data. Reuse the existing partner identity, native `res.currency`, ACLs, record rules, mail tracking, sequences, ORM row locks and SQL constraints. No database-name/hostname guards, cron, hooks or controllers.

A listing/job is not a `project.task`: native employee/project-sharing access and editable stages do not express public listings plus private offers. Native tasks remain the execution model in `authorize-contract-workspaces`; their stages never become the agreement lifecycle. Sale/Accounting are unnecessary. Project already depends transitively on rating; do not claim an installation lacks rating merely because this addon has no direct dependency.

### D2. Models and lifecycle

Profiles: unique partner, public name/headline/bio/skills, optional indicative rate/currency/country, availability, draft/active/suspended, published flag, manager verification badge and suspension reason/time. Owner activates a complete profile (name/headline/skill), marking `is_contractor` additively. Self-publication is not internal approval or work authorization. Suspension closes submitted proposals and leaves agreements historical; workspace integration additionally disables effective grants.

Jobs: reference; server-derived customer and company; title/description/skills; pricing type; optional budget bounds; active currency (default company currency); duration; portal/public visibility; lifecycle timestamps/reasons; assigned profile and accepted proposal. Customer creates draft without contractor verification. Draft → open → in_progress → delivered → done, with delivered → in_progress for requested changes. Customer/manager cancel draft/open; customer/contractor/manager cancel in_progress with reason; only manager cancels delivered. Done/cancelled are terminal. Uniform content lock applies while submitted proposals exist and after open, including manager typo edits.

Proposals: neutral reference, immutable job/profile, message, fixed/hourly amount > 0 in job currency, duration ≥ 1 day; submitted → accepted/withdrawn/declined/closed. Resubmit after withdrawal if currently eligible; never after decline. Close reasons: job_filled, job_cancelled, contractor_suspended. Partial unique indexes enforce one accepted per job and at most one submitted/accepted per job/profile. Contractor cannot bid on own commercial entity's opportunity. Exact customer ownership does not roll up to colleagues.

### D3. Security and mutation guard

Only manager group (`group_marketplace_manager`, implied for settings admins) receives generic mutation ACLs; public/portal/internal non-managers get read ACLs subject to rules. Protected state/ownership/assignment/timestamp fields require both a private operation context and an elevated environment. Caller context alone is untrusted. Private helpers start with `_`; all public methods derive actor from calling uid, check target access and allowlisted fields, acquire locks, recheck, and perform narrow elevated writes with real-actor audit. Generic manager edits must still obey content/lifecycle locks and record invariants.

Record read matrix: open public listings for everyone; open portal listings for authenticated users; exact customer sees own jobs; assigned contractor sees assigned jobs; proposals only their contractor/job customer; active published profiles and skills readable; own draft profile only its owner; manager sees records within permitted company scope. Add native company ceilings to job/proposal operations and record rules. Marketplace core does not claim database-wide isolation: the separate isolation addon supplies that for restricted internal users and must register these models/methods when composed.

Hide private partner relations, creator/editor references and follower metadata from unauthorized readers. Use safe per-caller projections (`is_customer`, `is_assigned_contractor`, `my_proposal_id`, owner/manager proposal count, participant customer display name), with viewer-aware caching and no sudo-search leakage. Neutral proposal display names; unreadable and missing targets give equivalent domain errors. Never give contractors a general contact directory.

### D4. Audit channels and files

Native mail.thread on profile/job/proposal; internal tracking and reason notes readable/postable only by managers, including when a participant is an internal user. No participant auto-followers. Block direct attachment create/relink on these models in every state and via message posting. Participant free text remains in explicit operation fields. `add-contract-negotiation` supplies a separate private conversation/document model; the core does not forbid those separately specified channels or weaken its own audit boundary for them.

### D5. Atomic acceptance and integration

Standalone acceptance checks exact customer (no manager/admin impersonation), submitted proposal, matching open job, active profile, currency/company eligibility. Lock job then proposals, invalidate cached transition fields, recheck, accept one, set assignment/time, close competitors and record audit in a single transaction. PostgreSQL uniqueness is the backstop; Odoo row-lock/serialization failures require a clean retry/refresh, never a partial winner. Independent-cursor tests must verify races, not just mocked locks.

Provide private extension points inside the authoritative public operation for preconditions and transactional effects. Negotiation requires current revision; workspace integration requires explicit work authorization and approved restricted identity. Its lock protocol adds user/profile locks before the job. Core job-only operations never take those locks after holding a job lock. Extensions override/adapt the public entry point so legacy calls cannot bypass their required inputs. Execution operations similarly consult the installed work-authorization policy. Standalone acceptance creates no task, collaborator or grant.

### D6. Backend and operation inventory

Manager-only menus for skills/profiles/jobs/proposals; reason wizard for suspend/reinstate/cancel/resolve and optional decline reasons. No customer-impersonating accept button. Owner/customer/contractor operations remain RPC-safe without a frontend. Profile methods create/update/activate/publish/unpublish; manager suspend/reinstate/verify. Job create/update/publish/unpublish/cancel/deliver/request-changes/confirm/manager-resolve. Proposal submit/update/withdraw/customer-decline/customer-accept. Reasons required for judgment-based manager transitions; participant pre-assignment cancel and decline reasons can be absent and must be audited as absent, not fabricated. Helpers are never remotely callable.

## Risks / Trade-offs

- [Risk] Native mail and attachment routes leak fields despite page filtering. → Generic RPC/mail/binary tests for public, portal and internal non-manager readers.
- [Risk] Rules traverse manager-only fields. → Early rule tests; use protected technical join fields if upstream field access prevents safe rule evaluation.
- [Risk] Acceptance races with proposal update/cancel/suspension. → Shared lock order, rechecks and real transaction tests.
- [Trade-off] Core still spans profiles through completion. → These are a coherent commercial transaction boundary with detailed tasks; optional reputation and required frontend/security extensions are independently tracked.

## Migration Plan

New additive sibling addon; no automatic promotion, historic task migration or publication. During approved apply, use an explicitly authorized disposable database and record installation, domain/RPC tests, concurrency and browser coverage. Keep the foundation installable alone. Destructive uninstall requires separate authorization; after real use preserve agreement/audit data. No production/database action is part of this planning run.
