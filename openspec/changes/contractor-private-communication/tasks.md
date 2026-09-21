# Tasks

## 1. Native mechanism verification

- [ ] 1.1 Create focused Odoo tests/probes for Proposal chatter, private Discuss channels, portal identities, followers, and Project chatter; record the mechanism that preserves each audience boundary.
- [ ] 1.2 Select and document the smallest safe supported mechanism; if none meets the boundary, stop and request a product decision.

## 2. Proposal and execution communication

- [ ] 2.1 Implement private Proposal communication for the customer commercial entity, that Proposal's Contractor, and authorized staff; verify Contract browsers and competing Contractors cannot read it.
- [ ] 2.2 Implement audience/lifecycle handling for submission, withdrawal, rejection, and acceptance; preserve proposal history without cross-Proposal access.
- [ ] 2.3 Implement post-award Project operational communication for the customer commercial entity, Assigned Contractor, and authorized staff without exposing Proposal history.
- [ ] 2.4 Expose authorized communication entry points without `sudo` bypasses and test portal/internal identities.

## 3. Verification

- [ ] 3.1 Run focused non-browser Odoo communication/security tests on a disposable database.
- [ ] 3.2 Run strict OpenSpec validation and `git diff --check`; update tasks only after implementation verification.
