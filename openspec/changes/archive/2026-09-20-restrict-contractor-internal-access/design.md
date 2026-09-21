# Design

## Context

The current code is an unverified baseline, not evidence that this change is
complete. Odoo ACLs are additive; record rules are the native per-record scope.

## Goals / Non-Goals

**Goals:** use one native Contractor group, normal ACLs and record rules, retain
the portal user's existing identity, and prove the role with focused tests.

**Non-Goals:** candidate recruitment, private negotiation, task CRUD after
assignment, customer portal creation, and a general-purpose authorization layer.

## Decisions

- Use normal groups, ACLs, and record rules. A narrow model guard is acceptable
  only where ACLs/rules cannot express a required denial, and must be tested.
- Inspect the Contractor group's effective implied groups and menus instead of
  assuming an internal baseline is safe.
- Activation changes the existing portal user and partner in place through an
  explicit authenticated action; it is never an approval queue.
- This change supplies only the base read boundary. The lifecycle change owns
  primary assignment, candidates, compensation, and Task CRUD.

## Risks / Trade-offs

- [Implied groups expose extra models] → inspect and test effective access.
- [Stored access-helper fields drift] → test recomputation and addon upgrade behavior.
- [Routes bypass ORM] → do not use `sudo` for Contractor Project/Task reads.

## Migration Plan

Upgrade `project_contractor` after implementation so stored fields, security
records, and views are synchronized; no identity migration is required.
