# Spec Delta

## MODIFIED Requirements

### Requirement: Minimal reusable presentation
The module SHALL supply functional, intentionally minimal QWeb portal/website
pages and navigation while preserving Odoo's normal authenticated `/my` portal
home routes. Branding, copy, layout, and styling specific to another site SHALL
remain outside the module.

#### Scenario: Generic page has no RAZS dependency
- **WHEN** a clean database renders a Contractor workflow page
- **THEN** it does not require RAZS templates, assets, or branding

#### Scenario: Contractor controller preserves portal home
- **WHEN** the Contractor portal controller is loaded
- **THEN** Odoo's `/my` and `/my/home` routes remain registered alongside `/my/contractor`
