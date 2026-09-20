# Spec Delta

## MODIFIED Requirements

### Requirement: Native communication reuse
The addon SHALL reuse an Odoo 19 Community native communication mechanism whose
tested membership and access behavior enforces the required private audience. It
SHALL NOT use Project followers, collaborators, or Project chatter for recruitment
unless that behavior has been tested to preserve the same boundary, and SHALL NOT
create a parallel custom messaging subsystem.

#### Scenario: Participant sends a message
- **WHEN** an admitted participant sends a recruitment message
- **THEN** it is delivered through the selected native mechanism only to the authorized audience
