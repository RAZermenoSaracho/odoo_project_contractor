# Spec Delta

## MODIFIED Requirements

### Requirement: Historical participation remains separate from award assignment

Historical task participation SHALL remain derived from task contractor
assignments and SHALL not be editable as a second historical source of truth.
The Project MAY additionally expose its one Assigned Contractor through its
accepted Proposal; that award relationship does not replace task-derived
participation history. Project candidate membership is not a recruitment or
authorization mechanism in the target workflow.

#### Scenario: Assignment does not rewrite history

- **WHEN** a customer's Proposal is accepted for a Project with no task contractor assignments
- **THEN** the Project has an Assigned Contractor and historical participation remains empty

#### Scenario: Project has no editable contractor field

- **WHEN** a project manager edits a Project
- **THEN** task-derived historical participation cannot be edited directly
- **AND** the separate award assignment follows its execution authority
