## Context

The two delta specs were moved intact from the unimplemented marketplace change during the 2026-09-18 reconciliation. Their policies remain useful but do not gate the required contractor workflow. No corresponding model currently exists.

## Goals / Non-Goals

**Goals:** immutable legitimate reviews, non-rewriting moderation, derived reputation, no private job/reviewer leakage.
**Non-Goals:** reverse reviews, paid ranking, editing submitted comments, payments, or mandatory review submission before completing work.

## Decisions

Sibling `project_contractor_reputation` depends on marketplace core, preserving that core's no-frontend dependency. Add `contractor.marketplace.review` with one row per job (unique constraint), rating 1–5, immutable comment/time/identities and manager-only private relations. Public read projection exposes rating/comment/time/profile only; participant rules use exact partners. Use the core protected-operation guard, internal-only audit, neutral sequence reference, attachment refusal and no auto-followers. `submit_review` derives customer/contractor, locks the job, requires done, and never expires eligibility. Hide/unhide changes visibility only; both operations require an audit reason. Deletion is forbidden.

Extend the profile with stored, protected reputation fields derived from completed jobs and visible reviews. Preserve the previous formulas: done count; visible review count; arithmetic rating average to two decimals; average assignment-to-completion days to one decimal; zero for empty sets. Display zero reviews as “no rating yet”. Updates recompute without cron and do not expose raw job/review relations. Verify that ORM recomputation does not become a generic write bypass.

Reuse native currency and the core lifecycle rather than sales/rating modules; native `rating.rating` has generic token-based semantics that do not by themselves enforce one immutable customer review per marketplace job. If the isolation layer is installed, register policies for the review model, methods and statistics; no implicit internal-user privileges. The core remains usable when this addon is absent.

## Risks / Trade-offs

- [Risk] Stored aggregates disclose private execution data. → Publish only the explicitly specified aggregate statistics and retain participant/admin restrictions on source relations.
- [Risk] Concurrent duplicate reviews or moderation. → Unique job constraint, locking and retry tests.

## Migration Plan

Install after marketplace core; no existing review migration is needed. Recompute initial profile statistics from legitimate existing completed jobs. Backend/API review operations are in scope; frontend review widgets are not a dependency of the required portal workflow. Preserve submitted content on moderation and retain audit on rollback.
