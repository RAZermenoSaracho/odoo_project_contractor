# Tasks

## 1. Verify and simplify the native foundation

- [x] 1.1 Audit the existing Contractor group, ACLs, record rules, models, and routes; remove unnecessary access machinery and verify through focused ORM access tests.
- [x] 1.2 Implement or correct self-activation of the current user/contact and verify repeat activation, foreign-user denial, and no duplicate identity.
- [x] 1.3 Implement and test own-partner read/write-only access and denial of foreign partner create/read/write/delete.

## 2. Base Project and Task boundary

- [x] 2.1 Implement and test Contractor read access to genuinely open Projects/Tasks and exclusion of Projects assigned solely to another Contractor.
- [x] 2.2 Implement and test the initial Project write boundary without Contractor changes to customer, assignment, reassignment, or closure.
- [x] 2.3 Inspect effective menus/models after activation and test that unrelated internal records are not granted by this addon.

## 3. Verification

- [x] 3.1 Run focused Odoo/Python tests on a disposable database with `project_contractor` installed and record results: clean install and upgrade of `contractor_access_clean_20260921` passed all 8 `TestContractorAccessControl` tests.
- [x] 3.2 Run strict OpenSpec validation and `git diff --check`; update tasks only after implementation verification.
