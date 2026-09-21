# Spec Delta

## ADDED Requirements

### Requirement: Authorized portal documents expose minimal Contractor identity
An authorized customer viewing a Contract, Proposal, or awarded Project SHALL
be able to see the referenced Contractor's display identity. This projection
SHALL expose only the Contractor identifier and display name and SHALL NOT grant
general access to that partner, unrelated partners, private profile fields, or
competing Proposals.

#### Scenario: Customer renders independent Contractor
- **WHEN** a customer opens an authorized Contract containing a Proposal from an independent Contractor
- **THEN** the page renders that Contractor's display name without granting partner-record access
