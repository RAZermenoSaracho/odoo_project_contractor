# Design

## Context

Odoo Project chatter, followers, and collaborators can expose an execution
workspace or subscribe users to its messages. They cannot be assumed to isolate
the private negotiations of competing Proposals for one published Contract.

## Goals / Non-Goals

**Goals:** use an existing Odoo message/channel model with exact Proposal
membership and keep post-award Project communication separate.

**Non-Goals:** custom message tables, standalone chat, a new attachment security
subsystem, public discussion, or outbound-commercial messaging.

## Decisions

- First verify Odoo 19 Community behavior for `mail.thread` on
  `contract.proposal`, portal identities, followers, and private
  `discuss.channel` with focused tests.
- Prefer Proposal chatter when its record access and follower behavior safely
  preserve the exact audience: authorized customer commercial-entity users,
  that Proposal's Contractor, and authorized staff. Do not use Contract or
  Project followers as recruitment audience unless tests prove the same boundary.
- Project chatter is evaluated separately as the operational audience after
  award: customer commercial entity, Assigned Contractor, and authorized staff.
- A private native Discuss channel is an acceptable fallback only if Proposal
  chatter cannot safely meet the boundary. It remains native infrastructure, not
  a custom messaging subsystem.
- Verification selected record-bound native chatter: both `contract.proposal`
  and the awarded `project.project` use `_mail_post_access = 'read'`, so a
  participant may post without receiving business-record write authority.
  Odoo 19 Community's `mail.message` access path then verifies parent-record
  access for searches and reads. Existing Proposal rules isolate each
  Contractor's record; the added customer execution-Project rule limits
  customer access to Projects linked to its commercial entity. No follower,
  channel, or general Discuss grant is used.

## Risks / Trade-offs

- [Portal chatter/Discuss limitations] → validate Odoo 19 Community portal access before implementation; if neither native option is safe, request a product decision.
- [Notifications persist outside Odoo] → revoke future channel access and document ordinary notification limits.
