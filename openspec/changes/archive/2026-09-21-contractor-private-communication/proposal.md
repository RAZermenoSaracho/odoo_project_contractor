# Proposal

## Why

Published Contract browsing must not expose negotiation. The product needs one
private customer-to-Contractor conversation per Proposal, and operational
communication after award, using native Odoo mechanisms rather than recreating
messaging.

## What Changes

- Investigate and adopt the smallest safe native Odoo mail/Discuss mechanism for each Proposal's private audience.
- Bind Proposal communication to the customer commercial entity, that Proposal's Contractor, and authorized staff only.
- Use Project chatter only for post-award operational communication, separate from Proposal negotiation history.

## Capabilities

### New Capabilities
- `contractor-private-communication`: Private native communication audience for recruitment.

### Modified Capabilities
- `contractor-communication`: Define concrete safe native mechanism and revocation behavior.

## Impact

Touches native Odoo mail/Discuss integration, Contract/Proposal access, Project
execution communication, portal authorization, and communication security tests;
no custom message store.
