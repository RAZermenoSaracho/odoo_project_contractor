# Spec Delta

## MODIFIED Requirements

### Requirement: Only an Assigned Contractor accesses an execution Project

A Contractor SHALL access an execution Project through being that Project's
Assigned Contractor. Contractors SHALL NOT browse unassigned Projects or use
Project candidate membership as a recruitment relationship. A Project assigned
to another Contractor SHALL be inaccessible through the Contractor role.

#### Scenario: Other Contractor cannot find Project

- **WHEN** Contractor B searches for a Project assigned to Contractor A
- **THEN** the Project is absent from B's Contractor-visible results
