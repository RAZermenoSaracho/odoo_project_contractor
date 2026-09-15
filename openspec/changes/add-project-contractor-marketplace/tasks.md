## 1. Phase 0: Prerequisites and foundations

- [ ] 1.1 Confirm the prerequisites before any implementation:
  - `add-project-contractor-foundation` is implemented and its tests pass;
  - the open-source license for both addons is approved;
  - the maintainer has decided the addon location: a sibling folder `project_contractor_marketplace/` in the `project_contractor` repository, or its own wrapper repository. If it moves repositories, move this change's directory along with it.

  Verify that the decisions are recorded in this change's design Open Questions (resolved) and that `openspec validate` still passes.
- [ ] 1.2 Get the maintainer's confirmation, then reuse or create the disposable test database (for example `project-contractor-test-odoo`) with `project_contractor` installed and without `website`. Verify the module list.
- [ ] 1.3 Create the `project_contractor_marketplace/__manifest__.py`:
  - `depends` exactly `["project_contractor"]`;
  - the approved license, category `Services/Project`, `application: False`;
  - no init hooks, no controllers;
  - `data` in load order (security XML, ACL CSV, rules XML, data, wizard views, views, menus), with each file registered as later tasks add it.

  Verify that installation on the test database succeeds and `tests/test_module_contract.py` asserts that `depends` is exactly `["project_contractor"]`, there are no init hooks, and no `ir.cron` belongs to the module.
- [ ] 1.4 Create `security/contractor_marketplace_security.xml`:
  - `res.groups.privilege` "Contractor Marketplace";
  - `group_marketplace_manager`, implying `base.group_user`;
  - `base.group_system` updated to imply it.

  Verify with a test that the admin user has the group, and a portal user and an internal non-manager don't.
- [ ] 1.5 Create `models/guard_mixin.py` (`contractor.marketplace.guard.mixin`) per design D6:
  - `_protected_fields` and the create/write guard (`env.su` plus the context key);
  - `_op_env()` with `mail_create_nosubscribe`;
  - `_check_allowed_values`;
  - `_resolve_accessible` (one generic `MissingError`);
  - `_post_audit`.

  Verify that the module upgrades and all helpers are `_`-prefixed. Behavioural coverage comes in 3.6.
- [ ] 1.6 Create `models/contractor_marketplace_skill.py` (`contractor.marketplace.skill`: name unique, sequence, active), with ACL (read for public, portal and user; CRUD for manager). There is no domain-specific seed catalog; demo tags go in `demo` data only. Verify with tests that the public user can search skills and a portal generic `create` raises `AccessError`.
- [ ] 1.7 Add `data/contractor_marketplace_sequence.xml` (`noupdate`) with the job, proposal and review sequences. Verify with a test that `next_by_code` returns each prefix.
- [ ] 1.8 Create `tests/__init__.py` and `tests/common.py` with fixtures:
  - a public user;
  - a portal customer and a same-company colleague;
  - portal contractors A and B;
  - an internal non-manager, a manager, and an admin;
  - an active non-company currency;
  - builders that call the domain operations only.

  All tests use `@tagged('post_install', '-at_install')`. Verify that `--test-tags /project_contractor_marketplace` runs with 0 failures.

## 2. Phase 1: Marketplace contractor profiles

- [ ] 2.1 Create `models/contractor_marketplace_profile.py` per design D3:
  - `mail.thread` and the guard mixin;
  - `UniqueIndex('(partner_id)')`;
  - manager-only `groups` on `partner_id` and `suspension_reason`, and on redefined `create_uid`/`write_uid`;
  - `hourly_rate` with a `res.currency` currency (active, company default);
  - `is_mine`, display name `public_name`, tracking, protected fields.

  Verify with a test that a second profile per contact is rejected.
- [ ] 2.2 Implement `create_my_profile`, `update_profile`, `action_activate` (which also sets the contact's foundation `is_contractor` in the operation environment), `action_publish`, `action_unpublish`, `action_suspend`, `action_reinstate` and `action_set_verified`. Activation and publication need no manager step and never check `is_verified`. Verify with `tests/test_profiles.py`: one test per scenario in `specs/marketplace-contractor-profiles/spec.md`, including "Activation marks the contact", "Suspension keeps the classification" and "Owner goes live without a manager". The suspension closure is in 4.4; the unverified bid is in 4.2.
- [ ] 2.3 Add profile ACL lines and rules (public, participant for `base.group_portal` and `base.group_user`, manager) to `security/contractor_marketplace_rules.xml` per D7. Verify the profile rows of `tests/test_access_matrix.py`.
- [ ] 2.4 Add an `@api.ondelete` guard: managers can delete only unreferenced profiles. Verify with a test.

## 3. Phase 1: Marketplace jobs (pre-assignment)

- [ ] 3.1 Create `models/contractor_marketplace_job.py` with every field in design D11:
  - `currency_id` referencing active `res.currency` records, defaulting to the company currency;
  - `visibility` defaulting to `portal`;
  - `contractor_partner_id` stored related, manager-only;
  - SQL CHECKs and constraints;
  - the sequence reference;
  - manager-only `groups` and `create_uid`/`write_uid`;
  - display name `[REF] title`;
  - `mail.thread` and `mail.activity.mixin` with tracking.

  Verify with a module upgrade and constraint tests.
- [ ] 3.2 Implement `create_job`, `update_job` (uniform edit lock), `action_publish` (never widens visibility), `action_unpublish` and pre-assignment `action_cancel`. Customer checks use the exact caller contact, and each operation locks the job row. Verify with `tests/test_jobs.py`: one test per scenario in `specs/marketplace-jobs/spec.md`, except those that need proposals, which are completed in 4.4.
- [ ] 3.3 Add the per-caller helpers `is_customer`, `is_assigned_contractor` (sudo-subquery `_search`) and `customer_display_name`, plus placeholders for `proposal_count` and `my_proposal_id` (implemented in 4.5). Verify with tests for "My Jobs listing" and the hidden customer display name.
- [ ] 3.4 Add job ACL lines and rules per D7, matching the exact `user.partner_id`. Verify:
  - the job rows of the access matrix, including the same-company colleague;
  - the test proving that rules traversing the manager-only `customer_partner_id` work for portal users. Apply the design fallback if it fails.
- [ ] 3.5 Create `models/ir_attachment.py`, refusing attachments on the four marketplace models in every state. Verify with tests for a manager on an open job and on a profile, and for `message_post` with an attachment.
- [ ] 3.6 Complete `tests/test_security_foundation.py`:
  - a manager's generic write to protected fields is rejected;
  - a manager's generic write to `name` succeeds;
  - `sudo().write` without the context key is rejected;
  - a portal generic `write`/`create` raises `AccessError`.

  Verify that the tests pass.
- [ ] 3.7 Add an `@api.ondelete` guard on jobs: only managers can delete, and only draft jobs that never had a proposal. Verify with tests.
- [ ] 3.8 Add `wizards/contractor_marketplace_reason_wizard.py` and its view, plus `views/` for skills, profiles and jobs and menus restricted to managers. Buttons call the operations. Verify in the test database browser (manager sees the menus, non-manager doesn't), and with a wizard delegation test.
- [ ] 3.9 Add the profile and job cases to `tests/test_privacy_leakage.py` (every readable field for the public user, another portal user and an internal non-manager). Verify that they pass.

## 4. Phase 2: Proposals and privacy

- [ ] 4.1 Create `models/contractor_marketplace_proposal.py` per D12:
  - partial unique indexes, CHECKs, sequence, neutral display name;
  - stored related currency;
  - `mail.thread` tracking;
  - `create_uid`/`write_uid`;
  - protected fields.

  Verify with a module upgrade and constraint tests.
- [ ] 4.2 Implement `submit_proposal(job_id, values)` with full eligibility (active profile, verification not required; job open and readable; not the customer or the same commercial entity; no active duplicate; no decline ever), re-run on every submission under the job lock. Verify with `tests/test_proposals.py`: one test per scenario in `specs/marketplace-proposals/spec.md`, plus "Unverified contractor can bid".
- [ ] 4.3 Implement `update_proposal`, `action_withdraw` and `action_decline`. Verify with tests for the update, withdraw and decline scenarios.
- [ ] 4.4 Add `_close_proposals(reason)`, wired into pre-assignment cancel and suspension, with edit-lock and unpublish checks counting `submitted` proposals. Verify with the tests for cancel with proposals, suspension closure, every edit-lock scenario, unpublish with pending proposals, and "Colleague cannot decide on proposals".
- [ ] 4.5 Add proposal rules and ACL lines (no public line); make `proposal_ids` manager-only; implement `proposal_count` and `my_proposal_id`. Verify the access-matrix proposal rows and the privacy scenarios.
- [ ] 4.6 Add proposal backend views for managers, with **no** accept button. Verify in the browser.
- [ ] 4.7 Add enumeration tests: neutral proposal display name, and identical errors for a foreign proposal and a nonexistent id. Verify that they pass.

## 5. Phase 3: Assignment, execution and completion

- [ ] 5.1 Implement `action_accept` per D13 (customer only, no group bypass) and `_close_competing_proposals`. Verify with `tests/test_assignment.py`: every non-concurrent scenario in `specs/marketplace-assignment/spec.md`, including manager and administrator refusal.
- [ ] 5.2 Add `tests/test_lost_race.py` (a patched `LockError` writes nothing; the unique-index backstop rolls back). Verify that it passes.
- [ ] 5.3 Implement `action_mark_delivered`, `action_request_changes`, `action_confirm_completion`, `action_resolve_done` and post-assignment `action_cancel`. Reject every transition on terminal states. Verify with `tests/test_execution.py`: every scenario in `specs/marketplace-job-execution/spec.md`, including the backdated delivered job, and participant cancellation refused after delivery.
- [ ] 5.4 Verify participant-only access after assignment with tests: a losing contractor is denied the job but can read their own proposal; the assigned contractor can read the customer's name.
- [ ] 5.5 Create the repository-root script `tests/concurrency_accept.py` (`odoo-bin shell`, two threads with independent cursors, 20 iterations). Verify exactly one accepted proposal per iteration.
- [ ] 5.6 Add execution buttons to the job form (manager: resolve and cancel through the wizard; no accept). Verify in the browser that the reasons appear in chatter.

## 6. Phase 4: Reviews

- [ ] 6.1 Create `models/contractor_marketplace_review.py` per D15:
  - unique job, rating CHECK, sequence;
  - manager-only `groups`, `create_uid`/`write_uid`;
  - tracking on `is_hidden`;
  - protected content, no deadline, no reverse direction.

  Add the job's `review_id`. Verify with a module upgrade and constraint tests.
- [ ] 6.2 Implement `submit_review`, `action_hide` and `action_unhide` (which write only `is_hidden` and `hidden_reason`). Verify with `tests/test_reviews.py`: every scenario in `specs/marketplace-reviews/spec.md`, including the hide/unhide round-trip and the manager rewrite refusal.
- [ ] 6.3 Add review rules and ACL lines. Verify the access-matrix review rows and the public leakage test.
- [ ] 6.4 Add review backend views (read-only content, hide/unhide through the wizard). Verify in the browser.

## 7. Phase 5: Reputation, hardening and documentation

- [ ] 7.1 Add the stored reputation computes on profiles per D16. Verify with `tests/test_reputation.py`: every scenario in `specs/marketplace-reputation/spec.md`.
- [ ] 7.2 Test that generic writes to reputation fields are rejected while recomputation still persists. Verify that the test passes.
- [ ] 7.3 Add `tests/test_rpc_surface.py` (`HttpCase`):
  - portal generic `create`/`write` rejected;
  - a private helper refused;
  - `submit_proposal` succeeds;
  - a manager's RPC `action_accept` rejected.

  Verify that the tests pass.
- [ ] 7.4 Complete the access matrix and privacy leakage tests across all models and actors. Verify that they pass.
- [ ] 7.5 Add `tests/test_audit.py`:
  - real-actor authorship;
  - reasons stored and posted;
  - no internal notes for portal readers;
  - no auto-followers;
  - participant message posts rejected;
  - participant attachments rejected.

  Verify that the tests pass.
- [ ] 7.6 Write the addon's open-source README:
  - scope and non-scope;
  - models and state machines;
  - the operations table;
  - the security model;
  - the confirmed decisions;
  - dependency direction and multi-currency;
  - obligations on presentation addons;
  - test commands;
  - no deployment branding.

  Verify that the operations table matches the implemented public methods.
- [ ] 7.7 Final verification. After confirmation, create a fresh, arbitrarily named database with `project_contractor` and `project_contractor_marketplace` only. Run `--test-tags /project_contractor_marketplace`, the concurrency script, and `openspec validate add-project-contractor-marketplace --strict`. Verify that installation succeeds, all tests pass, and validation reports no errors.
