# Design

## Context

The portal is a presentation layer over lifecycle and communication access. It
must not compensate for missing ORM security with elevated queries.

## Goals / Non-Goals

**Goals:** small generic authenticated pages completing the two defined user
journeys with native portal/website components.

**Non-Goals:** RAZS styling, anonymous marketplace browsing, browser automation,
custom frontend frameworks, payment, or a separate portal security engine.

## Decisions

- Use module-owned QWeb templates and authenticated controllers with CSRF-safe
  mutations. Query protected records as the requesting user where possible.
- Reuse `contract.contract.partner_id` for customer ownership. A customer user is
  authorized when their partner and the Contract customer have the same
  `commercial_partner_id`; express this through native partner hierarchy/domain
  semantics, not a custom organization or membership model.
- Customer controls create, edit, publish, and cancel Contracts; review and
  negotiate each Proposal; and accept one Proposal. Acceptance is the only
  customer action that creates an execution Project and assigns its Contractor.
  Contractor pages never offer those mutations.
- Contractor pages expose only published Contract projections, the requester's
  own Proposals, and execution Projects assigned to that Contractor. They do not
  expose Project candidate or unassigned-opportunity views.
- Contractor directory exposes an intentionally publishable profile projection,
  not arbitrary `res.partner` data.

## Risks / Trade-offs

- [Portal rules and controllers diverge] → test each route and avoid `sudo` except narrowly audited creation.
- [A broad partner hierarchy query leaks an unrelated entity] → test same-entity
  parent/child access and different-commercial-partner denial for every Contract,
  Proposal, and Project customer route.
