# Spec Delta

## MODIFIED Requirements

### Requirement: Generic single-addon delivery

The complete generic Contractor workflow, including Contract, Proposal, Project,
and later minimal portal pages, SHALL live in `project_contractor`. The addon
SHALL use its declared upstream Odoo dependencies and SHALL NOT require
`razs_web`, RAZS-specific records, branding, or another Contractor access addon.

#### Scenario: Clean generic installation

- **WHEN** `project_contractor` is installed on a normal compatible Odoo 19 Community database
- **THEN** its generic Contractor data and Contract/Proposal/Project workflow are available without RAZS-specific modules
