# Tasks

Planning only; all tasks below require explicit apply approval. Database work requires an authorized disposable target; no production changes are implied. Record actual verification results and skips before requesting archive approval.

## 1. Regression cases

- [ ] 1.1 Add direct company-history relation/count/action agreement tests with ordinary, archived, task-template and project-template work and active_test=False; verify they expose any current mismatch.
- [ ] 1.2 Add read-mutate-read cases without env.invalidate_all for reassignment, state, project, archiving/template and parent-contact changes; verify precisely which current compute paths become stale.

## 2. Consistency fixes

- [ ] 2.1 Make direct history relation, counts and actions share roll-up/exclusion semantics using readonly derived values; verify individual/company fixtures and viewer access still agree.
- [ ] 2.2 Unify Project contractor navigation with its computation work domain and readable project/task scope; verify template exclusions, archived context and no hidden-project identifier/count leakage.
- [ ] 2.3 Add minimal dependency or targeted invalidation needed by the reproduced mutation cases while retaining user/company context separation; verify same-transaction reads and cross-viewer tests pass.

## 3. Verification evidence

- [ ] 3.1 Run the complete foundation suite on an authorized disposable database, including native UI/RPC tests; record actual executed/passed/skipped results rather than inferring them from task checkboxes.
- [ ] 3.2 With separately authorized disposable install/upgrade/uninstall verification, record preservation of standard contacts/projects/tasks and contractor-data removal; run openspec validate fix-contractor-history-consistency --strict.
