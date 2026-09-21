# Tasks

## 1. Customer journey

- [x] 1.1 Implement customer ownership using matching `commercial_partner_id` values and authenticated Contract creation; verify same-entity parent/child contacts are allowed and foreign commercial entities are denied.
- [x] 1.2 Implement customer Contract lists, management, publication, Proposal review, Contractor directory projection, and invitation/contact; verify invitation only initializes a Proposal and does not assign.
- [x] 1.3 Implement customer-only Proposal acceptance, Contract cancellation, and Project commercial controls; verify Contractors cannot invoke them.

## 2. Contractor journey

- [x] 2.1 Implement generic activation/status and own-profile pages using the access foundation; verify no foreign contact data is exposed.
- [x] 2.2 Implement published Contract browsing and own-Proposal lists/actions; verify other Proposals and private negotiation are excluded.
- [x] 2.3 Link only authorized Proposal communication and assigned Project/Task work pages; verify controller behavior matches ORM rules.

## 3. Verification

- [x] 3.1 Run focused controller/ORM tests on a clean disposable Odoo database without browser automation.
- [x] 3.2 Run strict OpenSpec validation and `git diff --check`; update tasks only after successful implementation verification.
