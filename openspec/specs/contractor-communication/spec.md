# contractor-communication Specification

## Purpose

Provides private, native-Odoo communication for recruitment and active contract
work without exposing a Project's private discussion to every discoverer.

## Requirements

### Requirement: Private participant communication
Contract communication SHALL be readable only by the relevant customer,
admitted Participants/Candidates, the Assigned Contractor, and appropriately
authorized internal staff. Discovering an open Project SHALL NOT grant access to
its private negotiation or messages.

#### Scenario: Discoverer cannot read negotiation
- **WHEN** a Contractor discovers an open Project without being admitted as a Participant
- **THEN** that Contractor cannot read its private recruitment communication

### Requirement: Native communication reuse
The addon SHALL reuse Odoo mail, chatter, followers, project sharing, or Discuss
facilities where they meet the required audience boundary. It SHALL NOT create a
parallel custom messaging subsystem.

#### Scenario: Participant sends a message
- **WHEN** an admitted participant sends a recruitment message
- **THEN** it is delivered through the selected native Odoo communication mechanism to the authorized audience

### Requirement: Communication membership follows participation
Adding, withdrawing, assigning, or removing a Participant/Candidate SHALL add
or remove their private communication access consistently. Reassignment SHALL
not expose historic private communication to unrelated Contractors.

#### Scenario: Withdrawn candidate loses access
- **WHEN** a customer withdraws a candidate from a Project
- **THEN** that candidate can no longer access its private recruitment communication
