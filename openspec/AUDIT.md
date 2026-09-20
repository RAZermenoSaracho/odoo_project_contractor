# Contractor workflow rebaseline — 2026-09-20

## Scope

This is a planning audit. It changes OpenSpec artifacts only: no application
code, database, service, browser, or repository history was changed here.

`project_contractor` is the sole generic Odoo 19 Community addon. Its existing
contact classification, task contractor assignment, project participation, and
work-history features are retained as foundation behavior. Current code also
contains an unverified Contractor activation/access baseline. It is not treated
as verified completion in the open task lists.

## Product model

- A portal user explicitly activates the same user/contact as an internal
  Contractor; no approval or duplicate identity is involved.
- A `project.project` is the v1 Project/Contract. Its `partner_id` is the
  customer contact relationship; all portal users with the same
  `commercial_partner_id` are customer owners. It has zero or one primary
  Assigned Contractor and may have several Candidates.
- The lifecycle is **Discoverable → Participant/Candidate → Assigned Contractor**.
  These are authorization states. A small membership relation is permitted only
  if native Project relationships cannot safely express candidate admission and
  withdrawal.
- Compensation is only amount plus currency. Discussion uses native Odoo
  communication. There is no bid/proposal marketplace, billing, escrow,
  payment, milestone, or custom messaging subsystem.
- Historical task contractor fields and work history remain useful but do not
  replace primary Project assignment or candidate membership.

## Security matrix

| Contractor relationship | Project/Task | Private recruitment communication | Relationship changes |
| --- | --- | --- | --- |
| Discoverable | Read only permitted opportunity/Task information; no Project or Task mutation | None | None |
| Participant/Candidate | No Project or Task mutation | Customer, admitted candidates, assigned Contractor, and authorized staff only | None |
| Assigned Contractor | Operational Project write excluding customer, assignment/reassignment, and closure; Task CRUD in that Project | Authorized participant audience | None |

Contractors cannot access a Project assigned solely to another Contractor. They
can read/write their own `res.partner` profile only. Customers or authorized
internal staff control selection, reassignment, and closure.

Customer ownership is specifically the equality of the portal user's and the
Project customer's `commercial_partner_id`. It includes ordinary parent/child
contacts under one commercial entity and does not follow arbitrary contacts,
followers, candidates, collaborators, or Contractor classification.

## Odoo-native architecture

Use standard groups, ACLs, record rules, `project.project`, `project.task`,
`res.partner`, portal controllers/QWeb, and Odoo mail/Discuss. Project chatter,
followers, and collaborators require tests before being used for recruitment,
because they can widen Project or chatter visibility. The communication phase
will prefer a native private Discuss channel if its actual Odoo 19 Community
membership behavior meets the required boundary.

Do not add grant ledgers, custom authorization engines, global RPC interception,
HTTP route allowlists, attachment-security frameworks, or module inventories.

## Active change sequence

1. `fix-contractor-history-consistency` — retained focused maintenance work.
2. `restrict-contractor-internal-access` — verify/simplify automatic activation
   and native access foundation; all unverified work remains unchecked.
3. `contractor-project-lifecycle` — Project-as-Contract, candidates, one primary
   Contractor, compensation, and operation-specific Project/Task security.
4. `contractor-private-communication` — prove and integrate the safe native
   Odoo communication audience.
5. `contractor-portal-workflow` — minimal generic customer and Contractor pages.

The six previously abandoned overengineered planning changes remain removed:
`add-contract-negotiation`, `add-contractor-onboarding`,
`add-contractor-portal-workflow`, `add-marketplace-reviews-reputation`,
`add-project-contractor-marketplace`, and `authorize-contract-workspaces`.
They are not replacement implementation phases.
