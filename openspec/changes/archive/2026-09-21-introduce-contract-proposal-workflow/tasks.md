# Tasks

## 1. Contract and Proposal domain

- [x] 1.1 Add minimal `contract.contract` and `contract.proposal` models, native
  views/actions, amount/currency fields, state fields, mail-thread integration as
  needed, and declared upstream dependencies.
- [x] 1.2 Add native groups, ACLs, record rules, and narrow model transitions so
  customer commercial-entity ownership, published-Contract browsing, own-Proposal
  access, and authorized internal access are effective without privilege leaks.
- [x] 1.3 Implement Proposal draft, submission, withdrawal, rejection, and
  customer invitation-as-draft-Proposal behavior without a separate invitation model.

## 2. Award and Project execution migration

- [x] 2.1 Implement authorized, transactional, idempotent Proposal acceptance;
  record the accepted Proposal, reject competing active Proposals, and create one
  linked Project with the accepted Contractor assigned.
- [x] 2.2 Link Project, Contract, and accepted Proposal; keep Proposal amount and
  currency authoritative and preserve Assigned Contractor Project operational
  writes and Task CRUD while protecting commercial/relationship fields.
- [x] 2.3 Remove or simplify Project recruitment fields, candidate authority,
  unassigned Contractor discovery, and duplicate compensation behavior so
  Contractors access Projects only after award.
- [x] 2.4 Add an idempotent upgrade migration: convert compatible legacy assigned
  Projects to private awarded Contract/Proposal links, retire candidate-only data
  without fabricating Proposals, and leave ordinary Projects/task history intact.

## 3. Verification

- [x] 3.1 Add focused Odoo tests for Contract/Proposal state, commercial-entity
  customer ownership, Contractor and competitor isolation, invitation, and
  Proposal terms authorization.
- [x] 3.2 Add focused Odoo tests for acceptance atomicity/idempotence, competing
  Proposal transitions, Project linkage and visibility, Assigned Contractor Task
  CRUD, protected fields, legacy upgrade behavior, and existing work-history
  regression coverage.
- [x] 3.3 Run clean install and upgrade verification on disposable databases,
  then run the focused test suite without browser automation.
- [x] 3.4 Update OpenSpec tasks only after evidence, sync final requirements,
  archive the change when complete, and run strict OpenSpec validation plus
  `git diff --check`.
