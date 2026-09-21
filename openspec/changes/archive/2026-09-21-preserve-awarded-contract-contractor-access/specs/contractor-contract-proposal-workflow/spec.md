# Spec Delta

## ADDED Requirements

### Requirement: Accepted Contractor retains awarded Contract read access
The accepted Contractor SHALL retain ordinary read access to the originating
Contract after it transitions from published to awarded. Other Contractors
SHALL not discover or read that awarded Contract solely from a prior Proposal,
and published Contract discovery SHALL remain limited to published Contracts.

#### Scenario: Award preserves only winner access
- **WHEN** a customer accepts one submitted Proposal on a published Contract
- **THEN** the accepted Contractor can read the awarded Contract and reach their Proposal and Project, while competing and unrelated Contractors cannot read it
