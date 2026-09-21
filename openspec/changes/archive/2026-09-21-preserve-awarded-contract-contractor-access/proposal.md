# Proposal

## Why

Acceptance moves a Contract from published to awarded, causing the accepted
Contractor to lose the originating Contract record required by their Proposal
and Project journeys.

## What Changes

- Preserve read access to an awarded Contract only for its accepted Contractor.
- Keep marketplace discovery limited to published Contracts and preserve all
  competing and unrelated Contractor isolation.

## Capabilities

### Modified Capabilities
- `contractor-contract-proposal-workflow`: Retain accepted Contractor access to the awarded Contract.
