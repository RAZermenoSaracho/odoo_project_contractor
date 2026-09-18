## Context

See proposal.md. Current code defines no security objects. Local Odoo 19 source in `odoo/addons/project/security/ir.model.access.csv` grants `base.group_user` reads on tasks/projects; `project_security.xml` permits employee-visible projects/tasks. `odoo/odoo/addons/base/security/ir.model.access.csv` also grants internal attachment and reference-model access. Consequently, removing Project groups or hiding menus is insufficient. Odoo `orm/models.py` documents `_check_access` as an extension point, but searches/counts also use ACL and rule queries: a record-method override alone is insufficient.

## Goals / Non-Goals

**Goals:** a measurable access ceiling before account promotion; exact resource scope; ordinary employees unaffected; reusable policy extensions.
**Non-Goals:** onboarding UI, customer authorization, marketplace business objects, a universal sandbox for arbitrary trusted Python addons or malicious database administrators.

## Decisions

### D1. Separate security addon and persistent restricted identity

Use a sibling `project_contractor_access` addon depending only on the existing foundation. Keep the foundation's no-security-objects contract intact when installed alone. Store restricted-account status in a protected `res.users` field; a dedicated group provides menus/positive rights but is not the sole source of the restriction. Protect user type, direct and implied groups, allowed companies, partner relation and restriction changes. Use the existing user/partner; do not duplicate identity. No ordinary employee is automatically converted.

### D2. Native ACL and record-rule ceiling with a model policy registry

Use an explicit model/operation policy registry with default denial for restricted users. Extend the native model-access decision so an unlisted business model cannot inherit an additive `base.group_user` ACL. For reviewed models, add an AND restriction to effective record-rule domains, conditional on protected restricted status; it must participate in search, aggregate and direct-record checks. Do not rely on a contractor group rule, because other group rules are OR-ed. Preserve upstream company domains as additional constraints. `_check_access` can supply model-specific checks but must not be the only gate.

Policy categories are: bootstrap/reference read allowlist; own-user/own-partner limited fields and operations; public listing/profile projection; exact-grant protected resources; deny. Initially support the `project` dependency closure and foundation only; later addons explicitly register their policies and tests. Version the supported module/policy inventory. Invalidate policy/access caches on user, group, company, grant and module changes. Do not store a stale approval boolean as proof that current policy is safe.

### D3. Explicit grants and safe bootstrap

Use one grant model keyed by user, target model/resource, company, operation set, source authorization and revocation state; enforce uniqueness of an effective source/resource grant. Only private trusted operations create grants. Direct standalone security tests create them through private fixtures; this first change ships no administrator shortcut that impersonates customer authorization. Grant queries use narrowly scoped elevation internally to avoid recursive access checks, never arbitrary caller domains or resource models. Model names are allowlisted, not generic arbitrary-model pointers exposed to users.

For Project, grant a specific project and task set; no implicit child or sibling inheritance. Later workflow operations explicitly attach new tasks to a contract and grant them. Own-account access permits only approved preferences; user/group/company/partner administration remains forbidden. Reference exceptions contain no private commercial data. Restrict related-field and Many2one display-name exposures at the field/projection boundary as well as record level.

### D4. Entry points and elevated paths are part of verification

Native controllers and public model methods can elevate access or return data without ordinary reads. Maintain a reviewed callable-method/route surface for restricted users alongside model policies; unsupported business RPC methods/routes are denied before dispatch. Include binary/image/report/mail/discuss endpoints and generic CRUD/search/name-search/export methods in the inventory. Restrict those that can disclose unrelated data; do not assume `sudo()` becomes safe because a record rule exists. Narrow internal workflow elevation must first validate actor, target, fields and current grants and must retain real-actor audit attribution. Client-supplied context never signals trust.

### D5. Fail closed on incompatible configurations

Approval computes compatibility from the installed modules and effective group/policy surface. Unsupported additions prevent promotion and suspend protected-work operations for existing restricted users until reviewed; deny-by-default model and route policy remains effective during that interval. Do not generate permissive fallback rules. Module upgrades changing the policy surface require regression verification before re-enabling work. Before uninstalling the security addon, block removal while restricted accounts or grants remain; a separately authorized demotion/revocation operation must precede removal. Otherwise uninstall could turn restricted accounts into ordinary employees.

### D6. Verification contract

Build an access matrix with anonymous, portal customer, portal contractor, restricted A/B, ordinary internal employee, project manager and settings administrator across two customers, two companies and same-commercial-entity contacts. Exercise all CRUD, search/read/count/group/name-search/export/report/RPC/file/mail channels, context/group injection, grant revocation in existing sessions and module changes. Record model/route coverage and deliberately denied bootstrap paths. Failure to prove the ceiling blocks onboarding, not merely a test waiver.

## Risks / Trade-offs

- [Risk] Database-wide internal access is broader than Project. → Explicit model/method/route inventory and default denial; test actual installed module combinations.
- [Risk] Global restrictions break login, mail or reference rendering. → Explicit minimal bootstrap exceptions, own-account field restrictions and real browser tests.
- [Risk] Native or third-party elevated code bypasses rules. → Reviewed entry-point surface and unsupported-module refusal; no claim of safety for arbitrary server code.
- [Trade-off] More security work than portal-only collaboration. → Required by the requested internal-user transition; do not silently substitute portal-only access.

## Migration Plan

On explicit apply, install and test in an authorized disposable database only. Existing employees and foundation data remain unchanged. Introduce no automatic promotions. Rollback requires revoking grants and demoting workflow-managed accounts before removing the layer; preserve audits. No database work is authorized by the planning run.
