# Design

## Context

`ContractorPortal` extends Odoo `CustomerPortal`.  Python method overriding is
independent from the narrower route decorator, so its method must not reuse the
base controller's `home` name.

## Decision

Rename only the Contractor handler to `contractor_home`. Keep its route and
template unchanged. Test the generated Odoo route map rather than a browser.
