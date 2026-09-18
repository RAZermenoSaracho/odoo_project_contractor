# Project Agent Instructions

This repository uses this file as the authoritative source of project-level instructions for coding agents.

## Agent configuration

Reusable agent workflows are maintained under `.claude/`:

- `.claude/commands/` contains project slash-command workflows.
- `.claude/skills/` contains project skills and OpenSpec workflows.

Agents should reuse these existing files rather than creating equivalent or duplicated agent configuration elsewhere.

In particular, Codex should read and use the relevant resources under `.claude/` directly. Do not create or maintain duplicate `.agents/` copies unless explicitly requested.

## OpenSpec

This project uses OpenSpec for specification-driven changes.

OpenSpec is the authoritative methodology for planning and implementing changes.
Explore the existing code and specs first; create or update the proposal,
requirements/scenarios, design where appropriate, and actionable tasks; then
stop and present the plan for review. Do not implement application code until
the user explicitly instructs you to apply the change after reviewing the plan.
Use the existing OpenSpec apply workflow only after that instruction. Planning
completion and checked artifact status do not establish implementation completion.
Mark implementation tasks complete only when implemented and verified. Archive
only after implementation and verification are complete and the user explicitly
approves archiving. Preserve historical artifacts and report uncertain completion.

Before proposing, applying, updating, syncing, or archiving an OpenSpec change, inspect the corresponding workflow under `.claude/commands/` and `.claude/skills/` and follow the repository's existing OpenSpec conventions.

## Durable product intent

`project_contractor` is intended to provide a reusable, database-scoped contractor
workflow for Odoo 19 Community. External contractors work directly with customers
and may, after administrator approval, receive narrowly scoped internal access
to the database without unrelated internal-user visibility.

The intended workflow is:

1. A portal user registers or applies to become a contractor.
2. An administrator reviews the person and may approve their existing account as
   a restricted internal Odoo user. This grants no contract access by itself.
3. A normal authenticated portal customer creates or uploads a contract
   opportunity without needing contractor verification.
4. The customer browses the contractor directory and approaches one or more
   contractors. An opportunity may include an initial negotiable price.
5. Customer and contractor communicate and negotiate in a frontend/portal
   messaging experience. Contact grants no access to the protected workspace.
6. The customer accepts the agreed terms/price and explicitly authorizes work on
   that specific contract; only then does the contractor gain its scoped access.
7. Authorized work appears in the contractor's active-contract workflow, with
   clean backend and portal pages and navigation.

Authorization boundaries, record rules, portal/internal-user transitions,
multi-user visibility and prevention of accidental access to unrelated records
are core security requirements. Classification, directory publication, account
approval, negotiation and work authorization must never be conflated. Company
membership, followers, task assignment or an invitation must not implicitly
authorize unrelated work. Revocation must remove effective access.

The exact data model and UX are not predetermined: inspect implementation and
OpenSpec before choosing them, prefer native Odoo concepts and minimal extensions,
and explicitly spec any departure from the current foundation. Keep the addon
reusable on appropriate Odoo 19 Community databases without hosting, tenant, SSO,
database-name or deployment-branding assumptions.

The repository currently implements only the Contacts/Project foundation. Keep
current behavior distinct from planned capabilities in documentation. Main specs
describe the implemented baseline; unimplemented requirements belong in open
change deltas. `openspec/AUDIT.md` records the latest repository-based audit and
dependency order, not a substitute for each change's requirements.

## Repository safety

- Inspect existing repository conventions before modifying code.
- Do not commit or push unless explicitly requested.
- Do not modify unrelated files.
- Do not duplicate existing project configuration solely for compatibility with another coding agent.
