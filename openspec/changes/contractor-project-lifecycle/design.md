# Design

## Context

Odoo `project.project` already has a customer partner and native task relation.
Existing task `contractor_id` is useful history but cannot express a primary
Project Contractor or private candidate membership.

## Goals / Non-Goals

**Goals:** one Project as Contract, one primary Contractor, multiple candidates,
minimal compensation, and native operation-specific Project/Task authority.

**Non-Goals:** bids, offers, invoices, payment, escrow, milestones, or a
separate contract model.

## Decisions

- Extend `project.project` with primary Contractor, lifecycle, and monetary
  amount/currency. The upstream project customer remains the customer identity.
- Add a small Project-participant relation only if no native relation can track
  candidate admission/withdrawal safely; it is membership, not a marketplace.
- Keep historical `task.contractor_id` independent of primary assignment. Task
  operations are authorized by the Project primary Contractor once selected.
- Use operation-specific ACL/record rules: Discoverable read-only; Candidate
  communication-only; Assigned Contractor gets Task CRUD only in their Project.

## Risks / Trade-offs

- [ACLs are additive] → test every CRUD operation; use a small guard only when necessary.
- [Open information is sensitive] → portal phase defines a deliberately small public projection.

## Migration Plan

Add safe-default fields and upgrade normally. Map existing task-derived data
only if a separately tested migration rule is justified.
