# Spec Delta

## MODIFIED Requirements

### Requirement: Native communication reuse
The addon SHALL reuse an Odoo 19 Community native communication mechanism whose
tested membership and access behavior enforces the required private audience. It
SHALL prefer Proposal chatter when it safely preserves that boundary, SHALL NOT
use Contract or Project followers for recruitment unless tested to preserve the
same boundary, and SHALL NOT create a parallel custom messaging subsystem.

#### Scenario: Proposal participant sends a message
- **WHEN** an authorized Proposal participant sends a recruitment message
- **THEN** it is delivered through the selected native mechanism only to the authorized audience
