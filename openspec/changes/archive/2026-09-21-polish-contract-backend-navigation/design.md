# Design

## Context

The existing Contract action and forms are loaded by `project_contractor`, but
there is no Project menu entry, Contract smart-button navigation, or awarded
Contractor summary. Project award fields are currently rendered before the
standard notebook.

## Goals / Non-Goals

**Goals:** native Odoo actions, smart buttons, computed count/action pairs, and
a Project Contract notebook page using existing fields.

**Non-Goals:** changes to security, lifecycle transitions, stored relations,
portal/website presentation, chatter audiences, or custom styling.

## Decisions

- Add the menu beneath the existing Project application menu and point it to the
  current Contract action, so no separate application or permission path exists.
- Put navigation helpers on the models that own each relationship. Contract
  actions use direct Contract/Project/Proposal domains; Partner won-Contract
  data uses `accepted_proposal_id.contractor_id` and a non-stored computed count.
- Reuse standard `ir.actions.act_window` smart-button return dictionaries and
  target forms when exactly one linked record exists.
- Inherit the Project form notebook and insert a Contract page rather than
  changing the Project model or duplicating commercial data.

## Risks / Trade-offs

- [A user may lack access to a linked record] → actions use ordinary model
  access and record rules, so navigation never bypasses existing security.
- [A Contractor company may have child contacts] → the won count intentionally
  follows the exact accepted Proposal contractor relationship, not task-history
  company roll-up, because awards are the source of truth.
