## 1. Prerequisites and packaging

- [x] 1.1 Obtain the maintainer's approval of the open-source license (design D9 recommends LGPL-3; AGPL-3 is the alternative). Then replace the wrapper-root `LICENSE` with the approved license text and set the same identifier in `project_contractor/__manifest__.py`. Verify that the manifest `license` and the `LICENSE` text name the same license. No other task starts before this one is done.
- [x] 1.2 Get the maintainer's confirmation, then create the disposable test database `project-contractor-test-odoo` with only `project` installed (`odoo-bin -c <config> -d project-contractor-test-odoo -i project --without-demo=all --stop-after-init --http-port <free port>`). Verify that the module list shows `project` installed and `website`, `contacts` and `sale` not installed.
- [x] 1.3 Finalize `project_contractor/__manifest__.py`:
  - `name` "Project Contractors", `category` `Services/Project`, version `19.0.1.0.0`, a neutral summary and description;
  - `depends: ["project"]`, `application: False`;
  - no `pre_init_hook` or `post_init_hook`;
  - `data` listing only the view files added below.

  Delete the empty `controllers/` package and its import, and the header-only `security/ir.model.access.csv`, since the addon defines no models. Verify that `-i project_contractor --stop-after-init` on the test database succeeds.
- [x] 1.4 Create `project_contractor/tests/__init__.py` and `tests/common.py` with the fixtures from design *Test Strategy*: two companies, contractor and non-contractor partners, users of each access level, a portal collaborator, and projects with open, done, cancelled, archived and template tasks. Verify that `--test-tags /project_contractor` runs with 0 failures.

## 2. Contractor contact classification

- [x] 2.1 Create `models/res_partner.py`, adding `is_contractor` (Boolean, `index=True`, `default=False`, `copy=False`, label "Contractor", help explaining "external party performing project work") and a model helper returning the eligibility domain from design D2. Verify with a module upgrade and a test that new partners default to not being contractors.
- [x] 2.2 Create `views/res_partner_views.xml`, inheriting `base.view_partner_form` (the checkbox beside the standard classification fields) and `base.view_res_partner_filter` (a "Contractors" filter using the eligibility domain). No view is replaced. Verify in the test database browser that the checkbox and filter appear and work.
- [x] 2.3 Add `tests/test_contact_classification.py`, with one test per scenario in `specs/contractor-contact-classification/spec.md`. The "Unmark a contractor with past work" scenario is completed in 3.4. Verify that the tests pass.

## 3. Contractor task assignment

- [x] 3.1 Create `models/project_task.py`, adding `contractor_id` (Many2one `res.partner`, label "Contractor", `index='btree_not_null'`, `tracking=True`, `copy=False`, domain = eligibility + the same company domain as `partner_id`). Add `@api.constrains('contractor_id', 'company_id')` validating eligibility and company compatibility. Verify with a module upgrade and the tests "Non-contractor rejected" and "Contractor from another company rejected".
- [x] 3.2 Check task duplication, creation from a task template, and recurring-occurrence generation. If any path carries `contractor_id` over despite `copy=False`, clear it in that path. Verify with the test "Duplicate a contracted task", plus template and recurrence variants.
- [x] 3.3 Create `views/project_task_views.xml`, inheriting the task form (field beside `user_ids`), list (optional column), kanban (optional display) and search view (`contractor_id` field, "Contracted Work" filter, group-by Contractor). Verify in the test database browser.
- [x] 3.4 Add `tests/test_task_assignment.py`, with one test per scenario in `specs/contractor-task-assignment/spec.md`. The assignment-history test asserts:
  - a tracking value exists;
  - the contractor is not in `message_partner_ids`;
  - no `mail.mail` or `mail.notification` is created for the contractor.

  Verify that the tests pass.

## 4. Contractor project participation

- [x] 4.1 Create `models/project_project.py`, adding the non-stored `contractor_ids` (compute via `project.task._read_group`, not `task_ids`; excludes templates; no `sudo`), a `_search_contractor_ids` method, `contractor_count`, and `action_view_contractor_tasks`. Verify with the tests "Contractors from open and closed tasks" and "Archived and template tasks excluded".
- [x] 4.2 Create `views/project_project_views.xml`, adding a smart button (group `project.group_project_user`) to the project form that opens contracted tasks grouped by contractor, and a contractor search field. Verify in the test database browser.
- [x] 4.3 Add `tests/test_project_participation.py`, with one test per scenario in `specs/contractor-project-participation/spec.md`, including a test that no stored or editable contractor field exists on `project.project`. Verify that the tests pass.

## 5. Contractor work history

- [x] 5.1 Extend `models/res_partner.py` with `contractor_task_ids` (One2many, group `project.group_project_user`) and the non-stored `contractor_task_count`, `contractor_open_task_count`, `contractor_done_task_count` and `contractor_project_count`. They are computed with the upstream `child_of` roll-up and `_read_group` pattern (design D5), with no `sudo` and templates excluded. Add `action_view_contractor_tasks` (with open, done and all contexts) and `action_view_contractor_projects`. Verify with the tests "Company includes its contacts' work" and "Counts by state".
- [x] 5.2 Extend `views/res_partner_views.xml` with smart buttons in `button_box`, restricted to `project.group_project_user`. Verify in the test database browser: a project user sees the buttons with correct counts, and an internal user without Project access sees none.
- [x] 5.3 Add `tests/test_work_history.py`, with one test per scenario in `specs/contractor-work-history/spec.md` (including a reopened task, a changed contractor, a restricted project and a user without Project). Verify that the tests pass.

## 6. Access control, distribution and documentation

- [x] 6.1 Add `tests/test_access_control.py`, with one test per scenario in `specs/contractor-access-control/spec.md`:
  - read-only user;
  - no addon-owned groups, access rights or rules (queried through `ir.model.data` for module `project_contractor`);
  - portal user assigned as contractor;
  - multi-company.

  Add an `HttpCase` in which a portal collaborator reads a shared task, and a portal RPC request for `contractor_id`. Verify that the tests pass.
- [x] 6.2 Add `tests/test_distribution.py`:
  - manifest `depends == ["project"]`;
  - no init hooks;
  - no controllers package;
  - user-visible labels of added fields, filters and buttons contain "Contractor" and not "Contract ";
  - installing on existing data leaves assignees, customers, stages and states unchanged.

  Verify that the tests pass.
- [x] 6.3 Verify clean uninstallation on the test database, after the maintainer confirms: create contractor data, uninstall `project_contractor` through `odoo-bin shell`, and confirm every contact, project and task still exists with unchanged standard fields. Record the result in the change notes.
- [x] 6.4 Rewrite the wrapper-root `README.md` as the standalone open-source README required by `contractor-addon-distribution`:
  - purpose, and contractor vs. contract;
  - features and screenshots placeholders;
  - dependency, configuration (none) and usage;
  - known limitations (single contractor per task, no portal exposure, per-viewer counts);
  - license;
  - roadmap and relationship to `project_contractor_marketplace`;
  - no deployment branding.

  Verify it against the spec's README scenario.
- [x] 6.5 Final verification. After confirmation, create a fresh database with an arbitrary name (for example `project-contractor-verify-odoo`), install only `project` and `project_contractor`, run `--test-tags /project_contractor`, and run `openspec validate add-project-contractor-foundation --strict`. Verify that installation succeeds, all tests pass with 0 failures, and validation reports no errors.
