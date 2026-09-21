# Tasks

Planning only; all tasks below require explicit apply approval. Database work requires an authorized disposable target; no production changes are implied. Record actual verification results and skips before requesting archive approval.

## 1. Regression cases

- [x] 1.1 Add direct company-history relation/count/action agreement tests with ordinary, archived, task-template and project-template work and active_test=False; verified the original hidden-project count/navigation mismatch and the corrected shared exclusions.
- [x] 1.2 Add read-mutate-read cases without env.invalidate_all for reassignment, state, project, archiving/template and parent-contact changes; verified the existing targeted invalidation paths refresh immediately.

## 2. Consistency fixes

- [x] 2.1 Make direct history relation, counts and actions share roll-up/exclusion semantics using readonly derived values; verified individual/company fixtures and viewer access agree.
- [x] 2.2 Unify Project contractor navigation with its computation work domain and readable project/task scope; filtered grouped Projects through the viewer's Project access and verified exclusions, archived context, and no hidden-project identifier/count leakage.
- [x] 2.3 Add minimal dependency or targeted invalidation needed by the reproduced mutation cases while retaining user/company context separation; verified same-transaction refresh and existing multi-company filtering.

## 3. Verification evidence

- [x] 3.1 Run the focused non-browser history/participation and multi-company access suite on an authorized disposable database; 23 selected post-install test methods passed, with browser/UI automation intentionally excluded by the approved task scope.
- [x] 3.2 Verify clean install, upgrade, and uninstall on the isolated database; standard partner/project/task records survived and `is_contractor`/`contractor_id` columns were removed on uninstall. Strict OpenSpec validation passed.
