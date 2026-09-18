# Tasks

Planning only; all tasks below require explicit apply approval. Database work requires an authorized disposable target; no production changes are implied. Record actual verification results and skips before requesting archive approval.

## 1. Installable shell and navigation

- [ ] 1.1 Create the portal addon with workflow/portal/auth_signup dependencies and native portal layout; verify installation without deployment modules and foundation-only installation still works.
- [ ] 1.2 Add login/signup return flow and role-aware application/profile/directory/opportunity/conversation/active/completed navigation; verify disabled signup policy and portal-to-internal identity continuity.
- [ ] 1.3 Add application/status form and profile/directory pages using existing operations; verify applicant privacy, published-only directory and no general contact/user directory.

## 2. Customer and contractor pages

- [ ] 2.1 Add opportunity create/edit/upload and explicit document-audience controls; verify an ordinary portal customer with no contractor profile can complete the flow and uploads stay private.
- [ ] 2.2 Add selected-contractor outreach, separate conversation pages and structured offer/revision UI; verify A/B privacy, escaped content, currency rendering and read-only closed conversations.
- [ ] 2.3 Add current-terms preview and affirmative authorize-work confirmation with approval prerequisite/stale revision handling; verify contact/messages alone never create active work.
- [ ] 2.4 Add active/completed workspace/task/execution-message/document/delivery/customer-review pages; verify allowed actions and revocation are enforced after existing-session refresh.

## 3. End-to-end verification and delivery

- [ ] 3.1 Exercise forged POST/RPC, CSRF, GET-mutation, guessed URL and native download probes, plus counts/paging/search; verify server authorization matches visible actions with no elevated controller shortcut.
- [ ] 3.2 Run a complete multi-user browser journey from portal registration through admin approval, negotiation, explicit authorization, delivery, completion and revocation, including two customers/contractors/companies; record pass/skip evidence.
- [ ] 3.3 Verify keyboard-accessible forms, mobile layouts and empty/validation/concurrency states in browser; record observable results.
- [ ] 3.4 Document the top-level workflow installation and supported security/module matrix; verify arbitrary-name clean database navigation and run openspec validate add-contractor-portal-workflow --strict.
