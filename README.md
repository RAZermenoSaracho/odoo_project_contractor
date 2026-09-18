# Project Contractors for Odoo

| | |
| --- | --- |
| **Repository** | `odoo_project_contractor` |
| **Odoo addon** | `project_contractor` |
| **Odoo version** | 19.0 (Community) |
| **Addon version** | 19.0.1.0.0 |
| **License** | [LGPL-3](LICENSE) |

`project_contractor` is intended to provide a reusable, database-scoped contractor
workflow for **Odoo 19 Community**. External contractors should work directly
with customers and, after administrator approval, may become internal Odoo users
with access limited to explicitly authorized contracts, projects and resources.
They must not inherit general visibility into unrelated database records.

**Current implementation:** the addon is the contractor foundation described
below. The complete workflow is planned, not yet implemented.

## Intended end-to-end workflow

1. A portal user registers or applies to become a contractor.
2. An administrator reviews the application and may approve the existing person
   as a narrowly restricted internal user. Approval alone grants no contract access.
3. Any normal authenticated portal customer can create or upload a contract
   opportunity without contractor verification, browse the contractor directory,
   and approach one or more contractors.
4. An opportunity may include an initial proposed price. The customer and each
   contractor can discuss and negotiate terms through frontend/portal messaging.
5. Contact or negotiation grants access only to the deliberately shared brief
   and that private conversation, never to the customer's protected workspace.
6. The customer accepts the agreed terms/price and explicitly authorizes the
   contractor to work on that specific contract. Only then does its protected
   workspace become accessible and appear in the contractor's active contracts.
7. Backend and portal pages, navigation, revocation and verification must support
   this workflow cleanly on an appropriate Odoo 19 Community database, without
   deployment-specific identities, database names, hosting or SSO assumptions.

Authorization boundaries, record rules, portal/internal-user transitions,
multi-user visibility and prevention of unrelated access are core product
requirements. Contractor classification, directory publication, administrator
approval, negotiation and customer work authorization are distinct decisions.
The data model and UX should reuse native Odoo concepts with minimal extensions;
the reviewed OpenSpec changes define the implementation, not this overview.

## Implemented foundation

The current addon extends standard Odoo **Contacts** and **Project** so
external contractors can be recorded on contacts, assigned to tasks, and
followed across projects, **without being Odoo users**.

> **Contractors, not contracts.** A *contractor* here is an external person or
> company that performs project work. This addon is **not** about legal
> contracts, subscriptions, recurring contracts, or HR employment contracts.

## Why

In standard Odoo, a task links to two kinds of people: its internal
**assignees** (`user_ids`, which must be internal users) and its **customer**
(`partner_id`). There is no native place to record an outside freelancer or
subcontracting company that does the work, short of creating an internal account or
misusing the customer field or tags. This addon adds that missing
relationship with a small, upstream-safe extension.

## Features

### Contacts: contractor classification

- A **Contractor** checkbox on the contact form marks a person or a company as
  a contractor.
- Contacts that belong to a contractor company are eligible as contractors too,
  without their own checkbox.
- A contractor stays an ordinary contact: no user account, portal account or
  separate profile is created.
- A **Contractors** filter in the contact search lists eligible contractors.

### Tasks: external contractor assignment

- Each task has an optional **Contractor**: the one external contact performing
  it. It sits right after the assignees in the task form, and also appears on
  kanban cards and as an optional list column.
- Only active, eligible contractors that are shared or belong to the task's
  company can be set.
- Unmarking or archiving a contractor keeps it on tasks where it was already
  set.
- Work involving several contractors is split into subtasks, each with its own
  contractor.
- Task search adds a contractor field, a **With Contractor** filter and a
  **Contractor** group-by.
- Contractor changes are tracked in the task history. The contractor is never
  added as a follower and receives no email.
- Duplicated tasks, tasks created from templates, and recurring occurrences
  start without a contractor.

### Assignees versus contractors

| | Assignees (`user_ids`, upstream) | Contractor (`contractor_id`, this addon) |
| --- | --- | --- |
| Who | Internal Odoo users | Any eligible contact: person or company |
| Needs a user account | Yes | No |
| How many per task | Several | One (use subtasks for more) |
| Gets task access and notifications | Yes, through standard Project rules | No |

Setting or changing one never changes the other, nor the task's customer.

### Projects: participation and contractor history

- The project form shows how many contractors take part in the project,
  derived from its open and closed tasks (archived and template tasks
  excluded). The **Contractors** button opens that work grouped by contractor.
- Projects can be searched by contractor.
- A contractor's contact form shows its **Contractor Work** (open tasks),
  **Contractor Done** (completed tasks) and **Contractor Projects**. For a
  company, these include the work of its contacts. Cancelled tasks count as
  neither current nor completed.
- All of these values are computed from tasks and never stored or edited by
  hand.

## Current foundation security and privacy

- The addon adds **no new security groups, access rights or record rules**.
  Contractor data follows Odoo's standard Project and Contacts access.
- Participation and work-history values are shown only to **Project users**.
  They count only the tasks the viewing user may read, within the companies
  they are allowed to access.
- Being a contractor **grants nothing**: no user, no portal access, no follower
  subscription, no email.
- Contractor fields are **not readable by portal users**, including collaborators
  of shared projects, whether through the portal or RPC.

## Installation

Requirements: Odoo 19.0 Community with the **Project** app. No other module is
needed.

1. Clone the repository somewhere on your Odoo server:

   ```bash
   git clone https://github.com/RAZermenoSaracho/odoo_project_contractor.git
   ```

2. Add the cloned directory (the one containing the `project_contractor/`
   folder) to your Odoo `addons_path`, for example in your Odoo configuration
   file:

   ```ini
   addons_path = /path/to/odoo/addons,/path/to/odoo_project_contractor
   ```

3. Restart Odoo, then either install **Project Contractors** from the Apps
   menu (after *Update Apps List*, with developer mode enabled), or install it
   from the command line:

   ```bash
   odoo-bin -c /path/to/odoo.conf -d <database> -i project_contractor --stop-after-init
   ```

No configuration is required. Tick **Contractor** on the relevant contacts,
then set the **Contractor** of your tasks.

Uninstalling removes the contractor data only; contacts, projects and tasks stay
intact.

## Development and tests

The addon ships Odoo tests covering classification, task assignment, project
participation, work history, access control, distribution metadata, and a
headless-browser UI smoke test.

Run them against a disposable database:

```bash
odoo-bin -c /path/to/odoo.conf -d <test-database> -i project_contractor \
    --test-tags /project_contractor --stop-after-init
```

- The UI smoke tests (`tests/test_ui.py`) need Google Chrome or Chromium and the
  `websocket-client` Python package. Without them, those tests are skipped.
- The tests create and roll back their own data, but they install the addon, so
  never point them at a production database.

Design and requirements are documented with [OpenSpec](https://github.com/Fission-AI/OpenSpec)
under [`openspec/`](openspec/): current requirements in `openspec/specs/`, and
the history of implemented changes in `openspec/changes/archive/`.

## Known limitations

- One contractor per task; use subtasks for several contractors.
- Contractors are not given portal access to their tasks or history.
- Work-history counts differ between users with different project access.
- A contact of a contractor company is eligible without its own checkbox; the
  company's flag is what makes it eligible.

## Roadmap

The complete workflow is **planned but not implemented**. The existing
[`marketplace domain plan`](openspec/changes/add-project-contractor-marketplace)
and the other changes under [`openspec/changes/`](openspec/changes/) divide the
remaining work into independently verifiable capabilities. See the
[`repository audit and implementation order`](openspec/AUDIT.md).
The proposed packaging keeps this foundation usable alone and adds reusable
sibling addons for the workflow; installing the foundation alone does not
provide the complete product. Reviews and reputation are optional follow-on work.

Development follows a strict plan-before-code process: explore, prepare OpenSpec
proposal/specs/design/tasks, and stop for review. Implementation requires an
explicit subsequent instruction to apply a named change. Archiving requires
completed implementation, verification, and separate explicit approval.

## License

Copyright 2026 Ricardo Zermeño.

This addon is licensed under the
[GNU Lesser General Public License v3.0](LICENSE) (LGPL-3), the same license as
Odoo Community.
