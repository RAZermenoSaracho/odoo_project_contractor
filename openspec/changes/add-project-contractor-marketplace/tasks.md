# Tasks

Planning only; all tasks below require explicit apply approval. Database work requires an authorized disposable target; no production changes are implied. Record actual verification results and skips before requesting archive approval.

## 1. Core packaging and protection

- [ ] 1.1 Create sibling project_contractor_marketplace with LGPL-3 and depends exactly project_contractor, no controllers/hooks/cron; verify install without website and document transitive dependencies accurately.
- [ ] 1.2 Add manager group, ACLs, protected-operation helpers, reason wizard and neutral job/proposal sequences; verify real actor attribution, private helpers inaccessible over RPC, client context cannot unlock protected writes and ordinary internal users are not managers.
- [ ] 1.3 Build exact-partner/two-company fixtures for public, portal, internal non-manager and managers; verify the complete spec read matrix has explicit expected outcomes.

## 2. Profiles and opportunities

- [ ] 2.1 Implement generic skills and unique profile model with publishable content and protected partner/metadata fields; verify uniqueness, public projection and no contact-data leakage.
- [ ] 2.2 Implement profile create/update/activate/publish/unpublish/suspend/reinstate/verification operations and deletion guards; verify every profile scenario including portal self-publication without internal promotion.
- [ ] 2.3 Implement job fields, constraints, currency/reference/company defaults and customer create/update/publish/unpublish/cancel operations; verify customer needs no contractor verification, company spoofing fails and all job scenarios independent of proposals pass.
- [ ] 2.4 Implement profile/job rules, safe per-viewer read helpers and company ceilings; verify foreign drafts, same-company colleagues, counts/name lookup and metadata privacy.
- [ ] 2.5 Implement direct core attachment refusal and manager-only audit chatter for public/portal/internal participants; verify native mail/binary/message_post routes cannot leak or attach data.
- [ ] 2.6 Add backend skill/profile/job menus and reason actions, without customer-impersonating acceptance; verify manager browser navigation and non-manager denials.

## 3. Offers and assignment

- [ ] 3.1 Implement proposal fields, neutral names, protected relations and partial unique constraints; verify invalid amounts/durations and concurrent active duplicates are rejected.
- [ ] 3.2 Implement submit/update/withdraw/decline with shared job locking and eligibility including commercial self-bid exclusion; verify resubmission after withdrawal but never after decline and private proposal counts.
- [ ] 3.3 Wire cancellation/suspension closures and job edit/unpublish locks, including manager generic content edits; verify rollback, every pending-proposal lock scenario and terminal-state immutability.
- [ ] 3.4 Implement customer-only atomic acceptance with storage backstops and private integration hooks; verify manager/admin cannot act for customer, failures roll back all effects and standalone core creates no Project access.
- [ ] 3.5 Run independent-cursor acceptance-versus-acceptance/update/cancel/suspend races, with at least 20 repeated double-acceptance trials; record one-winner and no-partial-state results.
- [ ] 3.6 Add manager proposal views with no accept-as-customer action; verify customer/proposal-owner RPC operations and foreign-id enumeration resistance.

## 4. Execution and integrated verification

- [ ] 4.1 Implement deliver/request-changes/confirm/manager-resolve and post-assignment cancellation with timestamps/reasons; verify the full state matrix, no automatic completion and no participant cancellation after delivery.
- [ ] 4.2 Implement the execution authorization extension contract and test a policy fixture denying historical assignment after revocation; verify all public entry points consult the same installed policy.
- [ ] 4.3 Complete audit and access-matrix tests over all core models and read helpers; verify real authorship, no auto-followers, internal-note isolation and safe Many2one metadata.
- [ ] 4.4 Run install/upgrade, backend browser, ORM/RPC and concurrency suites on an authorized arbitrary-name disposable database; record skips separately and verify foundation-only installation remains supported.
- [ ] 4.5 Write the addon API/security README and record verification evidence; run openspec validate add-project-contractor-marketplace --strict and leave optional reputation/negotiation/workspace/frontend work in their own changes.
