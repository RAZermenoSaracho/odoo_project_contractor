# Tasks

## 1. Native mechanism verification

- [ ] 1.1 Create focused Odoo tests/probes for private Discuss channels, members, portal identities, followers, collaborators, and chatter; record the mechanism that preserves the audience boundary.
- [ ] 1.2 Select and document the smallest safe supported mechanism; if none meets the boundary, stop and request a product decision.

## 2. Recruitment communication

- [ ] 2.1 Implement private conversation creation and membership from customer, candidates, primary Contractor, and authorized staff; verify discoverers cannot read it.
- [ ] 2.2 Implement membership updates on invite, withdrawal, selection, and reassignment; verify unrelated Contractors never inherit private access.
- [ ] 2.3 Expose authorized communication entry points without `sudo` bypasses and test portal/internal identities.

## 3. Verification

- [ ] 3.1 Run focused non-browser Odoo communication/security tests on a disposable database.
- [ ] 3.2 Run strict OpenSpec validation and `git diff --check`; update tasks only after implementation verification.
