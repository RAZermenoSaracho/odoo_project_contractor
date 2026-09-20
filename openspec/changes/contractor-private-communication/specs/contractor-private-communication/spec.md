# Spec Delta

## Purpose

Adds private recruitment communication using an Odoo-native facility while
keeping discoverable Project information separate from negotiation.

## ADDED Requirements

### Requirement: Recruitment communication has an exact audience
Each Project recruitment conversation SHALL be limited to its customer,
admitted Candidates, Assigned Contractor if any, and authorized internal staff.
Discoverable Contractors SHALL not become members solely by viewing the Project.

#### Scenario: Discoverer is not a member
- **WHEN** a Contractor reads a Discoverable Project without an invitation
- **THEN** that Contractor is not a member of and cannot read its recruitment conversation

### Requirement: Native conversation membership is revocable
Withdrawing a candidate or replacing an Assigned Contractor SHALL remove their
future access to the Project's private recruitment conversation through the native mechanism.

#### Scenario: Candidate withdrawal
- **WHEN** a customer withdraws a candidate
- **THEN** the candidate can no longer retrieve the recruitment conversation
