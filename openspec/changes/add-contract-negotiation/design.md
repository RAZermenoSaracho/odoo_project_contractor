## Context

The revised marketplace core provides listings, proposals and atomic acceptance but no participant channel. Its listing/profile/proposal audit chatter and direct attachments remain closed. This change adds dedicated private models rather than making an open listing a private contract workspace.

## Goals / Non-Goals

**Goals:** customer-selected outreach, private pre-work discussion, controlled uploads, structured revision-aware offers.
**Non-Goals:** workspace access, automatic internal approval, arbitrary email recipients, document signing, payment processing or credential storage.

## Decisions

### D1. Separate conversation and file audiences

Create `contractor.negotiation` in sibling `project_contractor_negotiation` (`depends: project_contractor_marketplace`). Unique opportunity/profile relation; derive customer from opportunity and recipient identity from an eligible directory profile. Allow customer-owned draft outreach by storing an explicitly selected brief snapshot on the conversation; do not grant draft-job read access. A contractor can submit a proposal only when the opportunity is open as the core requires. Conversations belong to exact customer/contractor partners, not their commercial parents.

Use native `mail.thread` for the participant conversation with a strict server-controlled recipient set, no auto-followers and no automatic outbound email in the first delivery. A participant stream exposes only approved comment messages; internal notes remain manager-only even when the contractor has `base.group_user`. Core listing/proposal chatter remains internal-only. Public methods, mail store serialization, Discuss and generic message operations need the same policy; a secure custom page alone is insufficient.

### D2. Native attachment storage behind a private document record

Use `ir.attachment` storage linked to a new `contractor.document` policy record, not directly to a public-readable listing or proposal. Each document has customer ownership and an explicit audience: owner-private, one selected negotiation, or protected workspace. Sharing to several conversations creates explicit audience grants; it never infers access from all invitations. Protect create/write/unlink, copying, res_model/res_id changes, public flags, access tokens and binary reads. No bearer links for protected files. Validate PDF, plain text, JPEG and PNG content with a proposed 10 MiB/file limit; force safe download disposition and sanitized filenames, disallow HTML/SVG/executable uploads and MIME/extension mismatch. This is content handling, not a malware-scanning guarantee. Add optional scanning only through a separate reviewed integration.

Changing the audience is an owner operation with source and destination checks; do not let a generic attachment write bypass it. Customer-private files have no recipients until shared. Moving a document to workspace classification is not an invitation side effect. Revoke audience access on subsequent native and workflow download requests. No raw internal attachment ids are accepted as proof of ownership.

### D3. Price and offer revisions

Extend job editable inputs with `initial_price` (unset or positive), `price_negotiable` and keep native `currency_id`; retain the core uniform job-edit lock while proposals are submitted. Non-negotiable price constrains proposal amounts; pricing type must match the advertised fixed terms. Extend the existing proposal, not a second competing agreement model, with server-generated revision and immutable revision snapshots. Customer counteroffers are conversation requests; contractor confirmation updates a submitted proposal through its existing domain operation and produces a revision. Store original and revised values for participants separately from internal audit.

Acceptance takes the expected revision. Override the existing public acceptance entry so an old call without required revision fails cleanly when this addon is installed. Lock the opportunity, re-read offer/revision and recheck validity; stale terms roll back. Expose a private precondition/commit hook for the workspace addon; installing the full workflow makes explicit work authorization mandatory on every acceptance route. These are additive integration contracts already declared in the revised core spec; no standalone-core behavior is silently claimed to create Project access.

### D4. Terminal conversations and privacy

Acceptance/cancellation makes conversations read-only. Each losing contractor keeps their own snapshot/proposal, never execution fields. Winner execution messaging lives on a separate workspace channel added by the workspace change. Core customer identity fields stay protected; the conversation shows chosen participant display labels, not general contact references or contact details. No conversation action sets Project collaborator/follower/assignee relations.

## Risks / Trade-offs

- [Risk] `mail.thread` and `ir.attachment` have broad inherited APIs. → Test generic RPC and native mail/download endpoints, including restricted internal users, relinking and old tokens.
- [Risk] Revision racing with acceptance. → Shared job lock and revision comparison in the core acceptance path; real independent-cursor tests.
- [Trade-off] No outbound email or arbitrary file types in the initial channel. → Keeps the first usable negotiation scope independently verifiable; portal messaging and safe document upload still satisfy the workflow.

## Migration Plan

Requires implemented marketplace core. Existing proposals, if any, receive an initial server revision; existing core records have no attachments because the core refuses them. Do not infer conversations or document sharing from old proposals. Apply and verify on a disposable database before rollout; preserve revision/audit records on rollback.
