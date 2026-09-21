# Spec Delta

## MODIFIED Requirements

### Requirement: Native communication reuse
The addon SHALL reuse Odoo 19 Community record-bound native chatter on each
Proposal and awarded Project. Authorized participants SHALL be able to post
without receiving business-record mutation rights, while native message access
continues to enforce the parent record's ordinary ACLs and record rules. It
SHALL NOT use Contract or Project followers for recruitment, grant general
Discuss access, or create a parallel custom messaging subsystem.

#### Scenario: Proposal participant sends a message
- **WHEN** an authorized Proposal participant sends a recruitment message
- **THEN** it is delivered through the selected native mechanism only to the authorized audience
