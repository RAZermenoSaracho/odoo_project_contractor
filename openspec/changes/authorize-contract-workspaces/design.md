## Context

Native `contractor_id` is classification only. Marketplace acceptance currently records a commercial assignment without Project access. The isolation, onboarding and negotiation changes provide the primitives used here; see proposal.md.

## Goals / Non-Goals

**Goals:** exact agreement-bound access, native Project execution, no access on contact, complete revocation and accurate active work.
**Non-Goals:** silently sharing existing projects, multiple winning contractors on one opportunity, replacing contractors, payments, electronic signatures or making task stages the commercial lifecycle.

## Decisions

### D1. Dedicated workspace with native Project records

Sibling `project_contractor_workflow` depends on onboarding and negotiation. Use one dedicated `project.project` per authorized job and ordinary `project.task` records for execution; link both to a private authorization record. This avoids accidentally exposing unrelated records in an existing customer project. Avoid a second custom task engine. The marketplace job/proposal remain the commercial source of truth; a separate authorization record represents security state, not a duplicate lifecycle.

Store customer, contractor user, accepted proposal/revision, frozen terms, company, project and audit on the authorization; unique job/workspace mapping and no arbitrary record link inputs. The foundation `contractor_id` can be populated for reporting, but must never be used as the access grant itself. Project access is granted by the isolation layer and exact resource membership. Customer workspace reads use exact-owner policies in this addon, not broad portal commercial-parent sharing. Ordinary employees do not gain protected workspace access solely through employee-visible project defaults: use a conditional global ceiling for workflow-tagged projects/tasks/documents, with explicit administrator and customer/contractor policies. Non-workflow records retain upstream rules.

### D2. One acceptance path and lock protocol

The portal button means “Accept terms and authorize work”. Extend the existing proposal acceptance domain operation, rather than adding a bypassable parallel button. Inputs: proposal/revision and affirmative authorization, never customer/contractor/grant identity. Under a consistent lock order (contractor user, profile, job, proposals, authorization/grants), recheck account approval, active profile, company compatibility, current revision, customer ownership and job state. All participating suspension/revocation/acceptance operations use the same ordering. Core job-only operations lock job before proposals and must not subsequently acquire a user/profile lock.

Within that transaction accept exactly one proposal, freeze terms, close competitors, create the dedicated project/initial task, persist customer authorization and exact grants. A failed step rolls back all writes. Unique indexes prevent duplicate winners/workspaces. Retry an identical completed decision by returning its existing result only after rechecking actor and effective authorization; do not reactivate a revoked authorization. A different revision or competitor fails.

### D3. Limited execution surface

Contractor grant allows read on that project/task set, task execution state updates and controlled participant messages/documents/delivery. Generic writes to assignees, customer, contractor classification, ownership, project privacy, company, agreement and grants are refused. Do not add broad Project User/Manager groups merely for editable forms. Backend views call narrow operations; add positive task rights only with the restrictive field/record policy in force.

Customer task/resource creation is a domain operation on their authorization that records membership and adds exact grants atomically. New tasks are not implicitly accessible merely because they have the same project id. Execution thread is separate from internal Project audit chatter and negotiation history. Reuse the negotiation/document policy infrastructure with a workspace audience that tests effective grants, never widen a historical negotiation's audience.

### D4. Revocation and history policy

Keep accepted commercial terms immutable. Work authorization status can be active, revoked or completed; revocation does not fake cancellation or erase delivery. Revoke makes core execution operations unavailable until fresh customer reauthorization for the same contractor/terms. Cancellation revokes all protected work; completion downgrades to read-only for currently approved participants and removes active-list membership. Profile suspension disables effective work grants without changing accepted proposal/job history; reinstatement does not automatically revive revoked access. Approval revocation demotes to portal and removes all work access. User/company changes re-evaluate grants immediately.

All access checks derive effective permission from current approval, profile status, grant state and company scope. Invalidate rule/ORM caches after grant transitions. Already issued file URLs carry no access guarantee. Active list = exact caller, effective writable/work authorization, job in `in_progress` or `delivered`; completed read-only history is separate. Do not reuse foundation task counts as active-contract counts.

## Risks / Trade-offs

- [Risk] Customer's normal portal project sharing can include colleagues. → Workflow-specific exact-owner ceiling for marked workspaces, tested with same-company contacts.
- [Risk] Manager elevation bypasses customer acceptance. → No administrative assignment operation; managers may revoke or resolve delivery only as specified.
- [Risk] Deadlocks among suspension, acceptance and revocation. → Shared lock order and independent-cursor race tests before declaring ready.
- [Trade-off] One dedicated project per contract. → Simple first access boundary, with existing-project linking deferred rather than silently shared.

## Migration Plan

Never infer authorizations from historic task contractors, followers or accepted marketplace jobs. Existing accepted jobs need an explicit customer-authorized transition/migration before any workspace grant; first delivery can refuse legacy migration and show that requirement rather than fabricate consent. Preserve standalone foundation and core marketplace installs. Revoke grants before disabling integration; do not delete agreement/audit evidence.
