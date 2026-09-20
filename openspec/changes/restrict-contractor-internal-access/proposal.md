## Why

The previous access plan attempted database-wide isolation through a custom
policy inventory, grant ledger, RPC interception and route allowlists. That is
far beyond the product requirement and difficult to maintain.

## What Changes

- Extend `project_contractor` with one `Contractor` internal group and a
  portal self-service activation action for the user's existing identity.
- Use standard ACLs and global record rules to limit Contractor project/task
  visibility to their assignments and projects with no assignment.
- Limit Contractor contact access to their own partner record and provide small
  website pages for activation and the visible contract list.

## Out of Scope

Marketplace listings, approval workflows, negotiation, document sharing,
reviews, grants, module inventories and database-wide interception are not
part of this change.
