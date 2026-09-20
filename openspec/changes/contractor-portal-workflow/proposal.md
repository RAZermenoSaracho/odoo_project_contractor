# Proposal

## Why

The generic addon needs minimal functional customer and Contractor pages to make
the native lifecycle usable without relying on RAZS-specific presentation.

## What Changes

- Provide customer Project creation, ownership/participation lists, Contractor directory, invite/contact, and assignment controls.
- Provide Contractor activation, profile, discoverable/candidate/assigned lists, authorized communication, and work navigation.
- Keep templates minimal, generic, and reusable by a branded inheriting addon.

## Capabilities

### New Capabilities
- `contractor-portal-workflow`: Generic customer and Contractor workflow pages.

### Modified Capabilities
- `contractor-addon-distribution`: Deliver the complete generic workflow in one addon.

## Impact

Touches portal controllers, QWeb templates, native portal checks, and focused
controller/ORM tests; depends on lifecycle and communication phases.
