# Tasks

Planning only; all tasks below require explicit apply approval. Database work requires an authorized disposable target; no production changes are implied. Record actual verification results and skips before requesting archive approval.

## 1. Application model and review

- [ ] 1.1 Create the sibling onboarding addon depending on the verified access layer and the private application model with ownership/state constraints; verify duplicate concurrent pending applications are prevented.
- [ ] 1.2 Implement own draft/create/update/submit/withdraw and fresh resubmission operations with allowlists; verify spoofing, unrelated-user and commercial-colleague denials and preserved decision history.
- [ ] 1.3 Implement admin-only review list/form and reject operation with applicant-visible reason and separate private notes; verify marketplace managers without settings rights cannot review or approve.

## 2. Safe identity transitions

- [ ] 2.1 Implement approval using the isolation private transition API and user/application locks; verify same uid/partner, minimal effective groups, zero work grants and atomic rollback on incompatibility.
- [ ] 2.2 Implement revoke/demote and reapproval behavior; verify existing sessions lose protected work immediately, customer identity/history survives and old work grants do not reactivate.
- [ ] 2.3 Guard generic user/application writes and existing ordinary-employee conflicts; verify no self-approval, duplicate provisioning or silent removal of unrelated employee permissions.

## 3. Verification

- [ ] 3.1 Run application ORM/RPC and approval/revocation race tests, including native portal login and internal transition; record tested policy/module versions and confirm no implicit directory publication.
- [ ] 3.2 Run standalone access/foundation regressions and openspec validate add-contractor-onboarding --strict; record verification evidence and keep every unverified implementation task open.
