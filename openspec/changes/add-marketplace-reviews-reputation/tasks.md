# Tasks

Planning only; all tasks below require explicit apply approval. Database work requires an authorized disposable target; no production changes are implied. Record actual verification results and skips before requesting archive approval.

## 1. Optional review layer

- [ ] 1.1 Create optional reputation addon depending only on marketplace core and the unique immutable review model with protected metadata; verify core still installs alone and duplicate concurrent reviews cannot persist.
- [ ] 1.2 Implement derived-actor submit, manager hide/unhide with reasons, readonly content and delete/attachment guards; verify every review scenario including no deadline, no reverse review and exact hide/unhide content preservation.
- [ ] 1.3 Add public/participant/manager rules and backend moderation views; verify private reviewer/job/creator identity cannot leak through fields, display names, mail or RPC.

## 2. Derived reputation and verification

- [ ] 2.1 Implement stored protected profile statistics with immediate recomputation; verify all formulas, hidden/cancelled exclusion, no-rating display and rejected generic writes.
- [ ] 2.2 Register policies for restricted-user compositions and manager-only audit; verify native endpoints and real-actor attribution with existing access-layer fixtures.
- [ ] 2.3 Run complete review/reputation and core regressions plus duplicate/moderation races; record verification evidence and run openspec validate add-marketplace-reviews-reputation --strict.
