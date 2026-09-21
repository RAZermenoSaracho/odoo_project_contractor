# Proposal

## Why

The Contractor portal controller accidentally overrides Odoo's inherited portal
home handler, removing `/my` and `/my/home` while leaving `/my/contractor` live.

## What Changes

- Rename the Contractor-only handler so inherited Odoo portal-home routes remain registered.
- Add route-map regression coverage for the inherited and Contractor portal URLs.

## Capabilities

### Modified Capabilities
- `contractor-portal-workflow`: Preserve normal portal-home routing.
