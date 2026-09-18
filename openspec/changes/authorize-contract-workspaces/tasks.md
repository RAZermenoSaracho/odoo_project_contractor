# Tasks

Planning only; all tasks below require explicit apply approval. Database work requires an authorized disposable target; no production changes are implied. Record actual verification results and skips before requesting archive approval.

## 1. Authorization and Project boundary

- [ ] 1.1 Create workflow addon, unique authorization/workspace links and company constraints; verify generic create/write cannot fabricate customer authorization or link unrelated resources.
- [ ] 1.2 Implement exact-owner/customer and effective-contractor global ceilings on workflow projects/tasks/documents while preserving non-workflow upstream access; verify colleagues, ordinary employees and competing contractors cannot read protected work.
- [ ] 1.3 Implement atomic customer acceptance integration using the documented user/profile/job/proposal/grant lock order and affirmative authorization/current revision; verify rollback on failed workspace or grant creation and old RPC bypass denial.
- [ ] 1.4 Create dedicated native project/initial task and exact resource grants only inside authorization; verify one winner/one workspace and no grant through classification, followers or assignees.

## 2. Scoped work and lifecycle

- [ ] 2.1 Implement allowed contractor execution task operations and owner-scoped task/resource additions with atomic membership/grants; verify price/privacy/ownership/assignee/company mutations and unrelated create/delete are denied.
- [ ] 2.2 Add private execution participant messages and workspace document audience using existing conversation/document policy primitives; verify internal Project notes and other workspaces remain unreadable through native endpoints.
- [ ] 2.3 Implement customer/admin revocation and fresh same-contractor reauthorization with immutable terms; verify existing-session/file-URL denial, no manager reassignment and no implicit revival on profile reinstatement.
- [ ] 2.4 Integrate approval revocation, profile suspension, cancellation and completion with effective grants and core execution operations; verify completed read-only history, cancelled denial and blocked revoked delivery.
- [ ] 2.5 Implement active/completed contract search helpers, counts and restricted backend task/navigation views; verify the mixed-history scenario and direct-read/list/count agreement.

## 3. Verification and migration

- [ ] 3.1 Run independent-cursor competing acceptance and acceptance-versus-revocation/suspension races using shared lock ordering; verify no duplicate workspace, deadlock leakage or grant for an ineligible user.
- [ ] 3.2 Run cross-customer/company/colleague ORM/RPC/mail/binary/report/export probes with all layers installed and the foundation history fixes; record complete authorization matrix results.
- [ ] 3.3 Document no implicit migration of historic accepted jobs and safe revoke-before-disable procedure; verify fresh install and explicit legacy refusal and run openspec validate authorize-contract-workspaces --strict.
