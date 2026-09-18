## Why

The original marketplace plan forbids all participant messaging and uploads and has no customer outreach. A customer needs to share a brief with selected contractors and negotiate privately without granting access to the contract workspace.

## What Changes

- Add one private conversation per opportunity/customer/contractor, customer outreach to multiple contractors, and participant-only messaging.
- Add customer-owned uploaded documents with explicit per-conversation sharing and protected-workspace classification.
- Represent an optional initial negotiable price and revision-checked offers using marketplace proposals; never interpret a message or invitation as authorization.

## Capabilities

### New Capabilities
- `contract-negotiation`: Private outreach, messages, negotiable price and versioned offer confirmation.
- `contract-documents`: Private uploads, explicit audiences, safe downloads and revocation.

### Modified Capabilities
None.

## Impact

Depends on `add-project-contractor-marketplace`. New sibling addon `project_contractor_negotiation`, depending on `project_contractor_marketplace`; native mail and attachment primitives with explicit policies. Its capabilities add new private channels; they do not relax marketplace listing chatter/attachment prohibitions. Frontend pages are a later change.

Planning only. These decisions are proposed for review; implementation and archiving require separate explicit approval.
