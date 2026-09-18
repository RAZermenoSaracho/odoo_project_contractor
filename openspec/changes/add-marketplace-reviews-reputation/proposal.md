## Why

Reviews and reputation are useful but are not prerequisites for safe onboarding, negotiation and work authorization. Separate the existing detailed policy from the required workflow so each can be implemented and verified independently.

## What Changes

- Move the previously unimplemented marketplace review and reputation requirements into this optional follow-on change, preserving their policy.
- Add immutable customer-to-contractor reviews, audited visibility-only moderation and derived statistics.
- Keep private reviewer/job identity, concurrency constraints and internal audit safeguards.

## Capabilities

### New Capabilities
- `marketplace-reviews`: One immutable review per completed job and non-rewriting moderation.
- `marketplace-reputation`: Derived published profile statistics from completed jobs and visible reviews.

### Modified Capabilities
None.

## Impact

New sibling addon `project_contractor_reputation` depending on `project_contractor_marketplace`. Optional after the marketplace core; add portal review presentation only if the portal addon is installed through a separately reviewed integration, not a reverse domain dependency. No code exists or task is complete.

Planning only. These decisions are proposed for review; implementation and archiving require separate explicit approval.
