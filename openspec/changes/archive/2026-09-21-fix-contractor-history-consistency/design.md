## Context

See proposal.md. `res_partner.py` exposes `contractor_task_ids` as a plain inverse One2many: direct company reads omit child work and have no template exclusion. Counts/actions use a separate child roll-up and `_get_contractor_work_domain`. `project_project.py` navigation omits `has_project_template` and explicit active filtering while its count includes both. Both computed-history methods declare context dependencies only; tests of mutation call `env.invalidate_all()`. These are source findings, not runtime-confirmed failures.

## Goals / Non-Goals

**Goals:** consistent observable history and immediate refresh; retain normal record rules, company filtering, native task state and company roll-up.
**Non-Goals:** grant access, add portal history, change contractor eligibility or create a stored history ledger.

## Decisions

Use the shared work domain for every public history surface, including the direct task relation and Project navigation. Make the relation a readonly computed relation if needed to express company roll-up; it must not become an editable assignment surface. Preserve caller access and avoid sudo counts. Keep underlying task assignments authoritative.

Add the minimal dependency/invalidation mechanism for actual task changes, membership, state, archive/template flags and partner hierarchy. First reproduce read-mutate-read without blanket test invalidation, then use declared dependencies where they cover relationships; use targeted invalidation for search-derived cross-record values only where necessary. Preserve `uid` and `allowed_company_ids` context separation. Do not add a second stored counter or clear the entire registry cache to mask missing dependencies.

Test direct relation, action domains, counts and search under the same viewers. Include task/project templates, archived tasks with `active_test=False`, parent-contact moves and a task whose project itself is unreadable to the viewer. Project navigation/counts must not leak project identifiers or display names from a task the viewer can read.

## Risks / Trade-offs

- [Risk] Cache issue may differ by upstream invalidation path. → Regression evidence decides the minimal fix; the observable requirement remains the target.
- [Risk] Roll-up field changes affect consumers. → Preserve field name/read semantics and make the documented company behavior explicit; no write API is promised.

## Migration Plan

No new models or data migration. Apply after explicit approval; run the foundation suite in an authorized disposable database and record installation, upgrade, browser and uninstall checks with skips identified. Preserve archived artifacts as history rather than rewriting past completion claims.
