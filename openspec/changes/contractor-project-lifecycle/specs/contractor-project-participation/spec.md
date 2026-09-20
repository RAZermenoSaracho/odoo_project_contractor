# Spec Delta

## MODIFIED Requirements

### Requirement: No project-level contractor designations in v1
Historical task participation SHALL remain derived from task contractor
assignments and SHALL not be editable as a second historical source of truth.
The Project/Contract MAY additionally store one primary Assigned Contractor and
candidate membership for recruitment and authorization; neither value replaces
the task-derived participation history.

#### Scenario: Assignment does not rewrite history
- **WHEN** a customer selects a primary Contractor for a Project with no task contractor assignments
- **THEN** the Project has a primary Contractor and historical participation remains empty

#### Scenario: Project has no editable contractor field
- **WHEN** a project manager edits a Project
- **THEN** task-derived historical participation cannot be edited directly
- **AND** the separate primary Contractor and candidate controls follow their lifecycle authority
