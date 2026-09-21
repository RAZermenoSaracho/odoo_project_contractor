# contractor-project-participation Specification

## Purpose
Shows which external contractors take part in a project, derived entirely from the project's tasks, so the project level never holds a second, conflicting source of truth.

## Requirements

### Requirement: Participating contractors are derived from tasks
A project's participating contractors SHALL be the distinct contractors of its tasks, whether open or closed. Archived tasks and task templates SHALL be excluded. No user SHALL be able to edit the participating contractors directly. Any change to task contractors, task membership, archiving, or template status SHALL be reflected the next time the project is read.

#### Scenario: Contractors from open and closed tasks
- **WHEN** project P has an open task with contractor "Jane Doe", a done task with contractor "Acme Consulting", and a task without contractor
- **THEN** P's participating contractors are exactly "Jane Doe" and "Acme Consulting"

#### Scenario: Participation ends when the last assignment is removed
- **WHEN** "Jane Doe" is contractor of only one task of project P and that contractor is cleared
- **THEN** "Jane Doe" is no longer a participating contractor of P

#### Scenario: Archived and template tasks excluded
- **WHEN** the only task of P with contractor "Bob" is archived, and a task template of P has contractor "Dan"
- **THEN** neither "Bob" nor "Dan" is a participating contractor of P

#### Scenario: Cached participation refresh
- **WHEN** participation is read, the last task is reassigned or archived, and participation is read again in the same transaction without manual cache invalidation
- **THEN** the contractor set and count immediately reflect the changed eligible tasks

### Requirement: No project-level contractor designations in v1
Projects SHALL NOT store their own contractor designations (for example a primary contractor or a list of eligible contractors) in v1. Contractor participation SHALL have exactly one source of truth: task contractor assignments.

#### Scenario: Project has no editable contractor field
- **WHEN** a project manager edits a project
- **THEN** no contractor value can be entered on the project itself

### Requirement: Contractor count and navigation from the project
A project SHALL display the number of its participating contractors to users who can access the project's tasks. From the project, such a user SHALL be able to open the project's contracted tasks grouped by contractor.

#### Scenario: Open contracted work of a project
- **WHEN** a project user opens the contractors entry of project P, which has two participating contractors
- **THEN** the count shows 2, and P's tasks that have a contractor are listed grouped by contractor

#### Scenario: Navigation agrees with excluded tasks
- **WHEN** a project contains ordinary work, task templates and project-template tasks with contractors
- **THEN** the contractor navigation and count use exactly the same exclusions, including when archived-record filtering is disabled

### Requirement: Search projects by contractor
Project searches SHALL let users find the projects in which a given contractor participates.

#### Scenario: Projects of a contractor
- **WHEN** a project user searches projects for contractor "Acme Consulting"
- **THEN** exactly the readable projects with at least one non-archived, non-template task whose contractor is "Acme Consulting" are returned
