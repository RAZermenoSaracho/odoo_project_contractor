## Design

`project_contractor` depends on `project`, `portal` and `website`. It keeps
the existing user and partner: an authenticated portal
user posts to a CSRF-protected page, is marked as a Contractor, and receives
the Contractor group (which implies the normal internal-user group).

The addon uses ordinary Odoo ACLs for read/write-only Project and Task access.
Stored computed fields on projects collect users assigned on a task or through
the existing task contractor relationship. Global record rules are dynamic: for a
Contractor they permit assigned projects or projects without any contractor or
assignee; for every other user their domain is unrestricted. Task visibility
uses the corresponding task/project assignment condition.

The same pattern limits Contractor contact reads/writes to `user.partner_id`.
Because standard internal contact ACLs are additive, a short `res.partner`
`unlink` guard is necessary to guarantee that Contractors cannot delete their
own contact. No RPC monkey patch, HTTP route policy, attachment override,
grant model, module inventory, or custom access engine is used.

The website surface has three native authenticated routes: account status,
POST activation, and the visible-project list. Controllers do not use sudo for
project reads, so the displayed list is the same one protected by record rules.
