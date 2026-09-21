# contractor-project-lifecycle Specification

## Purpose

Defines the Contractor's execution authority after a Proposal has been awarded
and a Project has been created.

## Requirements

### Requirement: Only an Assigned Contractor accesses an execution Project

A Contractor SHALL access an execution Project through being that Project's
Assigned Contractor. Contractors SHALL NOT browse unassigned Projects or use
Project candidate membership as a recruitment relationship. A Project assigned
to another Contractor SHALL be inaccessible through the Contractor role.

#### Scenario: Other Contractor cannot find Project

- **WHEN** Contractor B searches for a Project assigned to Contractor A
- **THEN** the Project is absent from B's Contractor-visible results

### Requirement: Task authority is assignment-specific

The Assigned Contractor SHALL have create, read, write, and delete authority
for Tasks in their assigned execution Project. A Contractor without that
assignment SHALL have no Task mutation authority for the Project.

#### Scenario: Assigned Contractor creates a task

- **WHEN** the primary Contractor creates a Task in their assigned Project
- **THEN** creation succeeds

#### Scenario: Unassigned Contractor cannot edit Task

- **WHEN** a Contractor who is not assigned to the Project modifies its Task
- **THEN** the operation is denied
