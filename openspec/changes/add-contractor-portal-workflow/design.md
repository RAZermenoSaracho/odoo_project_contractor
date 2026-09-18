## Context

The current module ships backend inherited views only. Domain changes intentionally remain presentation-independent. This change supplies the reusable product frontend after their security and domain behavior are implemented.

## Goals / Non-Goals

**Goals:** complete reachable workflow using native portal layout, accessible forms and safe domain operations; preserve pages across portal/internal transition.
**Non-Goals:** custom identity provider, public auto-registration override, branded deployment, separate SPA, payment checkout or optional reviews blocking the release.

## Decisions

Create sibling `project_contractor_portal`, a documented top-level workflow installation target depending on `project_contractor_workflow`, `portal`, `auth_signup`. Reuse `portal.CustomerPortal`, `portal.portal_layout`, pager/search patterns and native auth redirects. Do not require website for portal forms unless a specific reviewed integration need emerges; never alter the standalone foundation manifest. Application review backend belongs to onboarding, Project work backend to workflow, marketplace moderation to core; this addon connects navigation rather than duplicating those operations.

Proposed routes: `/my/contractor/application`, `/my/contractor/profile`, `/my/contractors`, `/my/opportunities`, `/my/negotiations`, `/my/contracts`, with record detail and explicit POST actions. These are design choices for review, not existing routes. Login redirects retain a safe local return path. Directory is authenticated in this frontend even though core public projections may be readable; only active published profiles appear. Both portal and restricted internal users can use `/my` workflows according to their records.

Customer path: create opportunity → optional private upload → directory/approach → private conversation and structured offer → explicit terms-and-work-access confirmation → customer workspace review. Contractor path: apply/status and optional public profile → invitations/negotiations → admin approval when needed → active workspace → delivery/completed history. Keep negotiations and active contracts separate in the navigation and counts. Explain “awaiting internal approval” on attempted authorization without leaking application details. Display price with currency and pricing type; stale revision errors require refreshing terms, never silently accepting a newer price.

Controllers act as the request user. Domain methods derive actors, validate ids and enforce transitions. POST forms use CSRF; safe GETs only read. Uniform 404 on unknown/unreadable workflow targets; distinct validation/concurrency errors for readable records. No controller `sudo().write(request_values)` or token shortcut. Fetch display projections and counts under exact rights. Use sanitized message rendering and the controlled document download policy, including native-route checks supplied by the domain/security layers.

Browser acceptance fixture includes customers C1/C2 sharing a commercial entity, contractors A/B, administrator and ordinary employee, and two companies. Cover complete happy path plus guessed URLs, hidden controls via forged POST/RPC, competitor privacy, files, revoked sessions, paging/counts, keyboard navigation and mobile-width forms. Test frontend and backend after portal-to-internal transition. Log browser test skips as missing verification, never a pass.

## Risks / Trade-offs

- [Risk] Internal users are routed away from portal or get broader mail serialization. → Test both account types with the same page fixtures and private-note checks.
- [Risk] UX implies contact is work authorization. → Separate navigation, explicit confirmation and domain-enforced authorization.

## Migration Plan

Install the top-level addon on an authorized fresh arbitrarily named database and exercise the full workflow through shipped menus. Document addons_path, dependencies, supported security policy inventory and account revocation. Preserve existing users and standalone foundation behavior; no automatic account conversion or data publication.
