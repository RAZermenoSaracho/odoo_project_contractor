# Design

## Context

Odoo Project chatter, followers, and collaborators can expose the whole Project
workspace or subscribe users to its messages. They cannot be assumed to separate
a discoverable opportunity from private recruitment discussion.

## Goals / Non-Goals

**Goals:** use an existing Odoo message/channel model with exact membership and
make membership follow Project participation.

**Non-Goals:** custom message tables, standalone chat, a new attachment security
subsystem, public discussion, or outbound-commercial messaging.

## Decisions

- First verify Odoo 19 Community behavior for private `discuss.channel`, members,
  portal identities, followers, collaborators, and chatter with focused tests.
- Prefer one private native Discuss channel per Project recruitment conversation,
  linked from the Project/participant relation only as needed. Members are customer,
  admitted candidates, Assigned Contractor, and explicitly authorized staff.
- Do not use Project followers or collaborators as the recruitment audience unless
  tests prove they preserve the same boundary.
- The channel is native infrastructure, not a custom messaging subsystem. A small
  membership relation is justified only by the lifecycle state itself.

## Risks / Trade-offs

- [Portal Discuss limitations] → validate Odoo 19 Community portal access before implementation; if unsafe, request a product decision.
- [Notifications persist outside Odoo] → revoke future channel access and document ordinary notification limits.
