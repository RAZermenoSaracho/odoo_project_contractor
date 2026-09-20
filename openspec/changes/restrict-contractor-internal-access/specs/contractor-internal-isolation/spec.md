# Spec Delta

## Purpose

Establishes the small native Odoo Contractor access foundation needed before the
recruitment and portal workflow phases can safely extend it.

## ADDED Requirements

### Requirement: Explicit self-activation retains identity
An authenticated portal user SHALL be able to choose Contractor activation for
their own existing user and partner. The operation SHALL be idempotent, require
no administrator approval, and SHALL NOT create another user or partner.

#### Scenario: Activation is repeated
- **WHEN** the same portal user activates Contractor access twice
- **THEN** one unchanged user and one unchanged partner have Contractor access

### Requirement: Base access uses native Odoo security
The Contractor role SHALL use native groups, ACLs, record rules, and ordinary
model/controller behavior. It SHALL NOT introduce a grant ledger, RPC
interception, HTTP route allowlist, module inventory, or parallel authorization engine.

#### Scenario: Scoped ORM request
- **WHEN** a Contractor searches a protected Project or Task through the ORM
- **THEN** native ACL and record-rule evaluation determines whether it is returned
