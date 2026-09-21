# contractor-addon-distribution Specification

## Purpose

Makes `project_contractor` a portable Odoo 19 Community addon that supplies the
generic Contractor workflow without deployment-specific branding or companion addons.

## Requirements

### Requirement: Generic single-addon delivery
The complete generic Contractor workflow, including minimal functional customer
and Contractor portal pages, SHALL live in `project_contractor`. The addon SHALL
use its declared upstream Odoo dependencies and SHALL NOT require `razs_web`,
RAZS-specific records, branding, or another Contractor access addon.

#### Scenario: Clean generic installation
- **WHEN** `project_contractor` is installed on a normal compatible Odoo 19 Community database
- **THEN** its generic Contractor data, security, and customer/Contractor portal workflow are available without RAZS-specific modules

### Requirement: Required native dependencies
The addon SHALL declare the upstream dependencies needed for its Contract,
Proposal, Project, authenticated portal, and website workflow. It SHALL NOT depend on Sales, HR,
Accounting, payment, or a marketplace addon merely to provide the core workflow.

#### Scenario: No commercial subsystem prerequisite
- **WHEN** the manifest dependencies are inspected
- **THEN** they do not require invoicing, payment, escrow, or a marketplace subsystem

### Requirement: Extensible generic presentation
The addon SHALL provide intentionally minimal functional backend and website
views using standard Odoo mechanisms. A separate website addon MAY inherit and
brand those views without changing Contractor domain or access behavior.

#### Scenario: Branded addon can inherit
- **WHEN** a separate website addon customizes a Contractor template
- **THEN** the Contractor workflow remains supplied by `project_contractor`

### Requirement: Upstream-safe data extension
The addon SHALL extend standard Contacts, Projects, Tasks, and native
communication mechanisms without replacing their unrelated behavior. Existing
projects remain ordinary projects until an awarded Contractor workflow
relationship is set.

#### Scenario: Existing project remains unchanged
- **WHEN** the addon is installed with existing Projects
- **THEN** their standard owner, customer, tasks, and visibility are not reassigned by installation
