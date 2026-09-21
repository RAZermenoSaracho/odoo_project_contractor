# Design

## Context

The archived Project lifecycle correctly records the implementation that existed
at the time, but its Project discovery and candidate relationships put competing
Contractors near one shared workspace. The target separates a public customer
opportunity, one private negotiation per Contractor, and the awarded workspace.

## Goals / Non-Goals

**Goals:** small native Odoo models, commercial-entity customer ownership,
isolated Proposal records, one atomic award transition, and minimal migration
from the current Project-based recruitment implementation.

**Non-Goals:** bidding or scoring, payments, invoices, escrow, milestones,
custom authorization engines, custom messaging, or complete portal UX. Detailed
communication audience implementation remains in
`contractor-private-communication`.

## Decisions

### Domain model

- Add `contract.contract` with `partner_id`, a small state selection (`draft`,
  `published`, `awarded`, `cancelled`), `accepted_proposal_id`, and its one
  resulting `project_id`. `partner_id` uses normal
  `commercial_partner_id` parent/child semantics for customer ownership.
- Add `contract.proposal` with required `contract_id`, required Contractor
  partner/user relationship, state (`draft`, `submitted`, `accepted`,
  `rejected`, `withdrawn`), `amount`, and `currency_id`. It may inherit
  `mail.thread`; the next communication change verifies and implements the
  exact safe audience.
- A customer invitation is represented by creating or initializing the invited
  Contractor's draft Proposal. No separate invitation model is needed.
- A Contract has at most one accepted Proposal. A Proposal belongs to exactly
  one Contract and Contractor. The implementation will prevent duplicate active
  Proposal ambiguity for the same Contract/Contractor with native constraints
  and transition checks appropriate to the final Odoo model.

### Award and execution

- An authorized customer commercial-entity user or authorized internal staff
  accepts a submitted Proposal. The transition locks/checks the Contract,
  records its accepted Proposal, marks competing active submitted Proposals
  rejected, marks the Contract awarded, and creates one execution Project.
- `project.project` links to the Contract and accepted Proposal. Its Assigned
  Contractor derives from the accepted Proposal; the Proposal is the single
  authoritative source for agreed amount/currency. A Project may display
  read-only related terms but has no independently editable award terms.
- The award operation is transactional and idempotent: a retry returns the
  already linked Project. A uniqueness constraint or equivalent database-backed
  invariant prevents duplicate execution Projects per Contract/accepted
  Proposal.
- After award, Contractor Project record rules and narrow guards apply only to
  that Assigned Contractor. The existing assigned Project operational-write and
  Task CRUD behavior is retained. Customer, assignment, linkage, award terms,
  and closure fields remain protected.

### Retiring Project recruitment

- Remove or simplify Project `candidate_contractor_ids`, unassigned Project
  Contractor discovery, Project candidate record rules/guards, and Project
  recruitment compensation/lifecycle fields. Contractors no longer reach
  Projects before award.
- Preserve task-level contractor assignment and derived work-history behavior;
  it remains historical data and does not become a second award source.
- Existing Project candidate relationships cannot be safely converted into
  Proposals because they lack an individual consented negotiation record and
  terms. They are retired rather than fabricated.

### Migration and compatibility

- For an existing Project with a current primary Contractor, create a private
  awarded legacy Contract and accepted Proposal using the current customer,
  Contractor, amount, and currency, then link the Project. This preserves the
  existing awarded access relationship without inventing competing proposals.
- Existing unassigned or candidate-only Projects remain ordinary Projects and
  are not automatically published as Contracts: their prior visibility does not
  establish current customer intent. Their Project recruitment access is removed;
  a customer or staff member can create a new Contract if recruitment is wanted.
- The migration shall be idempotent, preserve unrelated standard Projects and
  task/history records, and be covered by upgrade tests.

## Risks / Trade-offs

- [Commercial-entity portal domains vary by Odoo portal implementation] → test
  same-commercial-partner allowance and unrelated-commercial-partner denial at
  ORM/controller boundaries before portal work.
- [Mail/chatter followers can be broader than record access] → the following
  communication change must prove Proposal and Project audience behavior before
  exposing it in the portal.
- [Legacy candidate data has no Proposal equivalent] → intentionally retire it
  with documented migration behavior instead of creating false negotiation data.
