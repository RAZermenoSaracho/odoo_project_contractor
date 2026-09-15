## Why

The `project_contractor` foundation (change `add-project-contractor-foundation`) lets Odoo record external contractors on contacts and tasks. Some deployments also want a **marketplace** on top of it:
- customers post work;
- contractors with public profiles submit proposals;
- one proposal is accepted;
- work is delivered and confirmed;
- the customer reviews the contractor.

That layer brings public and portal exposure, private negotiation, a strict lifecycle, and reputation. None of that belongs in the generic foundation, so it is planned as a separate, **optional** open-source addon, `project_contractor_marketplace`.

Every business rule and privacy guarantee must hold at the ORM/RPC boundary. Portal users can call any public model method through `/web/dataset/call_kw` (`auth="user"`), so website or portal controllers can't be the security boundary.

This change was originally drafted as `add-contractor-marketplace-domain` for a deployment-specific addon. It was renamed and re-scoped when the foundation became a generic addon. Its Odoo 19 research, security model and confirmed policy decisions are kept. **It is not implemented as part of the foundation.**

## What Changes

This change is **planning only**. It is implemented after the foundation, by a later `/opsx:apply`.

- **New optional addon `project_contractor_marketplace`**, depending only on `project_contractor`. It owns:
  - marketplace contractor profiles;
  - marketplace jobs and their lifecycle;
  - proposals and proposal privacy;
  - atomic acceptance and assignment;
  - execution, delivery and completion;
  - reviews and reputation;
  - marketplace groups, ACLs, record rules, invariants, audit trail, and an explicit domain API.

  It ships no website templates, controllers, branding, hosting, SSO, or payments.
- **Built on the foundation's identity.**
  - A contractor is a contact classified by `project_contractor`.
  - A marketplace profile is an optional 1:1 public-facing record for that contact, holding only data the contractor publishes.
  - Activating a profile marks the contact as a contractor.
  - No second identity and no user requirement beyond the portal login used to act in the marketplace.
- **Own marketplace models, not `project.task`.** Jobs, proposals and reviews are dedicated models with explicit state machines. Project tasks can't express public listings with private proposals, and their stages are freely editable. Handing an accepted job off to a `project.task` (with the foundation's task contractor) is a documented extension point, not v1.
- **Deny-by-default mutation surface.** Portal and public users get read-only ACLs scoped by record rules. Every change goes through explicit, RPC-safe operations that check the actor and accept allowlisted values. Lifecycle, assignment, ownership and reputation fields can't be written generically, not even by managers.
- **Proposal privacy, atomic assignment, two-step completion, immutable reviews, derived reputation**, each specified with the confirmed policy decisions below.
- **Confirmed marketplace policy decisions (2026-09-14), kept as they were:**
  1. contractors self-activate and publish;
  2. jobs are owned by the individual contact;
  3. logged-in visibility is the default;
  4. job details are locked while proposals are pending;
  5. resubmission after withdrawal but never after decline;
  6. customer-only acceptance;
  7. no automatic completion;
  8. no cancellation after delivery;
  9. customer-to-contractor, immutable, deadline-free reviews with non-rewriting moderation;
  10. no messaging or attachments in v1.
- **Generic, not deployment-specific.** The earlier Odoo-consulting fields (Odoo-version catalog, Odoo-specific work types) are removed; deployments add such vocabulary as skill tags or downstream extensions. The addon depends on no hosting, tenant, SSO or website module, and never checks database names or topology.
- **Money.** Standard `res.currency` relations, with the company currency as default only. No payment logic.

## Capabilities

### New Capabilities
- `marketplace-contractor-profiles`: optional 1:1 public profile for a contractor contact. Covers its publishable content, self-service lifecycle, verification badge, and marking the contact as a contractor.
- `marketplace-jobs`: the marketplace job (individual ownership, content, currency, default and explicit visibility, publish, edit lock, unpublish, cancel before assignment).
- `marketplace-proposals`: submission eligibility (including resubmission), content, update, withdraw, decline, the state machine, and proposal privacy.
- `marketplace-assignment`: atomic, concurrency-safe acceptance of exactly one proposal by the customer only.
- `marketplace-job-execution`: delivery, change requests, customer confirmation, no automatic completion, no participant cancellation after delivery, manager resolution, timestamps.
- `marketplace-reviews`: one immutable customer-to-contractor review per completed job, with non-rewriting moderation.
- `marketplace-reputation`: contractor statistics derived only from completed marketplace jobs and visible reviews.
- `marketplace-access-control`: actors, the read matrix, no generic mutation, protected fields, identity privacy, enumeration resistance, and no attachments or messaging.
- `marketplace-domain-api`: the operation inventory, derived actors, allowlists, error semantics, frontend and topology independence, dependency direction, and additive integrations.
- `marketplace-audit-trail`: timestamps, tracked fields, recorded reasons, real-actor attribution, and internal-only audit.

### Modified Capabilities
_None._ There are no archived specs. This change assumes the foundation's capabilities (`contractor-contact-classification`, `contractor-task-assignment`) exist once that change is archived.

## Impact

- **New addon `project_contractor_marketplace`**. Its location is decided before implementation: either a sibling addon folder in the `project_contractor` repository (OCA-style multi-addon repo) or its own wrapper repository.
- **Prerequisite:** `add-project-contractor-foundation` is implemented. The license for both addons is approved.
- **Dependencies:** `project_contractor` only, which brings in `project`, `mail` and `portal`. No `website`, `sale`, `account`, `rating`, hosting, or deployment-specific module.
- **Downstream consumers** (for example a deployment's website or portal addon) depend on this addon, never the reverse. They must call the domain operations as the request user and never `sudo()`-write marketplace records.
- **Operational:** no cron jobs, external services or credentials. The addon installs in any database whatever its name.
