## Purpose

Makes the contractor foundation addon installable and useful on any compatible Odoo 19 Community installation with Project, as a clean open-source module with no deployment-specific assumptions.

## ADDED Requirements

### Requirement: Minimal dependencies
The addon SHALL declare exactly one dependency: `project`. It SHALL NOT depend on website, portal-page, contacts-app, sales, HR, accounting, or any non-upstream module.

#### Scenario: Declared dependencies
- **WHEN** the addon's manifest is inspected
- **THEN** its dependencies are exactly `project`

#### Scenario: Install where only Project is present
- **WHEN** the addon is installed in a database that has only `project` and its own dependencies installed
- **THEN** installation succeeds and every contractor capability works

### Requirement: No deployment or data assumptions
The addon SHALL work regardless of database name, hostname, hosting setup, or installed website. It SHALL NOT refer to specific projects, stages, users, companies, or other records by identifier, except records the addon itself defines or standard upstream reference data. It SHALL NOT require portal users or website pages.

#### Scenario: Arbitrary database
- **WHEN** the addon is installed in a new database with an arbitrary name, its own projects, and its own task stages
- **THEN** installation succeeds and contractors can be classified, assigned, and reviewed in work history

### Requirement: Upstream-safe extension
The addon SHALL add its fields and interface elements by extending the standard Contacts and Project models and views, without replacing upstream views or changing the behavior of existing upstream fields. When no contact is marked as contractor and no task has a contractor, Contacts and Project SHALL behave as without the addon.

#### Scenario: Existing projects unaffected
- **WHEN** the addon is installed in a database with existing projects and tasks
- **THEN** no contact is a contractor, no task has a contractor, and existing assignees, customers, stages and states are unchanged

### Requirement: Clean uninstallation
Uninstalling the addon SHALL remove its contractor classification, task contractor values, and interface additions. It SHALL leave contacts, projects, and tasks otherwise intact.

#### Scenario: Uninstall after use
- **WHEN** the addon is uninstalled from a database where contractors were assigned to tasks
- **THEN** all contacts, projects, and tasks still exist with their standard data unchanged

### Requirement: Contractor terminology and open-source documentation
User-visible labels SHALL use "Contractor" for the external party performing work, and SHALL NOT present the feature as legal contracts, subscriptions, or employment contracts. The addon SHALL ship a README that explains:
- its purpose;
- the difference between contractors and contracts;
- its features;
- its dependency;
- configuration (none required) and usage;
- known limitations;
- its license;
- its relationship to the optional marketplace addon.

The addon and its documentation SHALL contain no deployment- or organization-specific branding.

#### Scenario: Labels say contractor
- **WHEN** the addon's user-visible field labels, filters and buttons are reviewed
- **THEN** each refers to contractors, and none refers to contracts

#### Scenario: README completeness
- **WHEN** the README is reviewed
- **THEN** it covers each listed topic and names no specific organization's deployment

### Requirement: Consistent open-source license
The license declared in the addon's manifest SHALL be the approved open-source license, and it SHALL match the license file shipped at the repository root.

#### Scenario: License consistency
- **WHEN** the manifest license and the repository license file are compared
- **THEN** they name the same approved open-source license
