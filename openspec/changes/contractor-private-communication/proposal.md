# Proposal

## Why

Open Project discovery must not expose negotiation. The product needs private
customer-to-candidate communication, but Odoo-native communication must be
selected and scoped carefully rather than recreated.

## What Changes

- Investigate and adopt the smallest safe native Odoo mail/Discuss mechanism for a Project's private candidate audience.
- Bind communication membership to customer, candidate, assigned Contractor, and authorized staff.
- Keep recruitment messages separate from the discoverable Project projection.

## Capabilities

### New Capabilities
- `contractor-private-communication`: Private native communication audience for recruitment.

### Modified Capabilities
- `contractor-communication`: Define concrete safe native mechanism and revocation behavior.

## Impact

Touches native Odoo mail/Discuss integration, Project participation, portal authorization,
and communication security tests; no custom message store.
