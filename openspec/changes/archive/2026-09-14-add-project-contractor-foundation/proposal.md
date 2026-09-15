## Why

Standard Odoo 19 Community has no way to say that a contact is an external contractor, or that a project task is performed by one, unless that person becomes an Odoo user. The only people linked to a task are internal assignees (`user_ids`, which must be internal users) and the customer (`partner_id`). Teams that subcontract project work end up misusing the customer field or tags, or creating paid internal users for outsiders.

`project_contractor` fills that gap as a small, reusable, open-source extension of Contacts and Project. It is the foundation that a later, optional marketplace addon (`add-project-contractor-marketplace`) builds on.

"Contractor" here means an **external party who performs project work**. The addon is not about legal contracts, subscriptions, recurring contracts, or employment and HR contracts.

## What Changes

- **Rename.** The scaffold addon and its repository are renamed from `razs_contracts` to `project_contractor`, with RAZS branding removed. The addon targets any compatible Odoo 19 installation with Project.
- **Contractor classification on contacts.** `res.partner` gets a simple contractor flag. A contractor stays an ordinary contact: either a person or a company. Contacts belonging to a contractor company count as that company's contractors. No user account, profile model or second identity is created.
- **Contractor on tasks.** `project.task` gets one optional contractor (a contact): the external party performing that task. It is separate from the internal assignees (`user_ids`), which keep their standard meaning. Work involving several contractors is split into subtasks, as Odoo already does for internal work. The contractor field's presence is itself the marker for contracted work.
- **Contractor participation on projects.** `project.project` shows which contractors take part in it, computed from its tasks. There are no redundant stored or manually maintained project fields.
- **Contractor work history.** A contractor contact shows its tasks, open (current) work, completed work and projects, including its contacts' work for a contractor company. Everything is computed from task records under the viewer's normal access rights.
- **Access and privacy.** No new groups, models or record rules. Contractor data follows standard Project and Contacts access. Flagging a contact grants it nothing: no user, no portal access, no follower subscription, no email. Contractor fields are not exposed to portal or project-sharing users.
- **Distribution.** `depends` is `project` only. Nothing assumes a database name, hosting topology, website, portal users, specific projects or stages, or any deployment. Views extend upstream views rather than replacing them, and the addon ships a standalone OSS README.
- **Marketplace moved out.** The earlier marketplace plan (jobs, proposals, acceptance, reviews, reputation, and its security machinery and policy decisions) is **not** part of this change. It continues, restructured, as `add-project-contractor-marketplace` for the separate optional addon `project_contractor_marketplace`.
- **License.** At planning time the scaffold carried a placeholder proprietary license, which conflicts with open-source distribution. The license was changed only after the maintainer approved a choice (gating task 1.1): **LGPL-3** was approved.

## Capabilities

### New Capabilities
- `contractor-contact-classification`: marking contacts (persons or companies) as contractors, company-to-contact eligibility, and finding contractors in Contacts.
- `contractor-task-assignment`: one optional external contractor per task, eligibility validation, and separation from internal assignees and the customer. Also covers subtasks, tracking, and no automatic notifications.
- `contractor-project-participation`: contractors participating in a project, derived from its tasks, with navigation and search.
- `contractor-work-history`: a contractor's tasks, current work, completed work and projects, derived from task records with company roll-up and without stored counters.
- `contractor-access-control`: contractor data inherits standard Project and Contacts access. Covers no implicit access, users or notifications for contractors, and no exposure to portal or project-sharing users.
- `contractor-addon-distribution`: minimal dependencies, no deployment or topology assumptions, upstream-safe view inheritance, clean install and uninstall, and open-source documentation.

### Modified Capabilities
_None._ The repository has no archived specs yet.

## Impact

- **This repository**:
  - repository and addon directory renamed from `razs_contracts` to `project_contractor` (the repository is published as `odoo_project_contractor`; the installable addon stays `project_contractor`);
  - manifest identity metadata and README rewritten neutrally;
  - implementation (tasks) adds model extensions, inherited views and tests, updates `depends` to `["project"]`, and removes the unused `controllers/` package.
- **Other OpenSpec change**: `add-contractor-marketplace-domain` is renamed to `add-project-contractor-marketplace` and re-scoped to the optional marketplace addon. It is not implemented by this change.
- **Outside this repository (not edited here)**: downstream, deployment-specific modules that referred to the old scaffold name must update those references themselves. The foundation addon is reusable and makes no assumptions about any deployment.
- **Dependencies**: `project` (which provides `mail`, `portal`, `resource`, `analytic`, …). No `website`, `contacts`, `sale`, `hr`, or custom modules.
