# Tasks

Planning only; all tasks below require explicit apply approval. Database work requires an authorized disposable target; no production changes are implied. Record actual verification results and skips before requesting archive approval.

## 1. Private outreach and messages

- [ ] 1.1 Create the negotiation addon, unique conversation model and exact participant rules with private brief snapshots; verify concurrent outreach produces one thread per contractor and draft outreach does not expose the draft job.
- [ ] 1.2 Implement owner-only outreach and explicit brief sharing to one or more active published recipients; verify supplied customer identity, unrelated opportunity and competing contractor probes fail.
- [ ] 1.3 Implement participant message operations and safe mail serialization with manager-only internal notes and no arbitrary recipients/auto-followers/email; verify native mail/Discuss and generic RPC preserve thread privacy for portal and restricted internal users.
- [ ] 1.4 Implement read-only closure on acceptance/cancellation and retain only own snapshots/proposals; verify losing-contractor history reveals no execution data.

## 2. Private documents

- [ ] 2.1 Create the private document/audience model and controlled ir.attachment storage; verify initial owner-only upload requires no contractor verification and core direct-attachment refusal remains intact.
- [ ] 2.2 Implement upload content/size validation, explicit per-conversation sharing and relinking/public/token guards; verify prohibited files, foreign attachment reuse and partial-failure orphan cleanup.
- [ ] 2.3 Implement current-rights download/preview/binary policy, including native endpoints; verify revoked shares and guessed ids return no bytes, filenames or private metadata.

## 3. Offer revisions

- [ ] 3.1 Add optional initial price/negotiability with native currency and existing edit locks; verify unset versus zero, non-negotiable mismatch and pending-proposal edit denial.
- [ ] 3.2 Add immutable proposal revision snapshots and participant-visible structured revisions; verify customer counteroffer messages cannot modify contractor terms and every submitted revision preserves audit.
- [ ] 3.3 Extend the authoritative acceptance entry with expected-revision validation and rollback; verify stale/no-revision legacy RPC calls cannot accept changed terms, including update/accept races.

## 4. Verification

- [ ] 4.1 Register the negotiation/document method and model policies for composed restricted-user installations; verify no unsupported model or native route is implicitly allowed.
- [ ] 4.2 Run all negotiation, attachment, message and revision ORM/HTTP/race tests and core regressions; record verification evidence and run openspec validate add-contract-negotiation --strict.
