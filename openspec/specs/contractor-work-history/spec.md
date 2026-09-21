# contractor-work-history Specification

## Purpose
Gives each contractor contact a view of the project work it performed and is performing: tasks, current work, completed work and projects. It is derived from task records and never maintained by hand.

## Requirements

### Requirement: Contractor tasks with company roll-up
A contact SHALL expose the tasks for which it is the contractor. For a company, this SHALL also include tasks whose contractor is any contact belonging to that company, following the same parent-contact roll-up Odoo applies to a customer's tasks. Archived tasks and task templates SHALL be excluded.

The task relation returned by a direct read, the history actions and counts SHALL
all use these same roll-up and exclusion rules, even when the caller disables the
usual archived-record filter.

#### Scenario: Individual contractor tasks
- **WHEN** "Jane Doe" is contractor of tasks T1 and T2
- **THEN** Jane's contractor tasks are exactly T1 and T2

#### Scenario: Company includes its contacts' work
- **WHEN** "Acme Consulting" is contractor of task T3 and its contact "Bob" is contractor of task T4
- **THEN** Acme's contractor tasks are T3 and T4, and Bob's are only T4

#### Scenario: Direct company history and exclusions
- **WHEN** a company and its child contact have ordinary, archived, task-template and project-template assignments and a user reads the company history directly or through navigation
- **THEN** every surface includes the readable ordinary company/child work only, including with archived-record filtering disabled

### Requirement: Current and completed work
A contractor's work SHALL be classified from each task's own state:
- **current work**: tasks that are not closed;
- **completed work**: tasks in the done state;
- cancelled tasks count as neither current nor completed, but remain in the contractor's task list.

The contact SHALL expose the number of current and completed tasks, and SHALL let the user open each set.

#### Scenario: Counts by state
- **WHEN** a contractor has one in-progress task, one task with changes requested, two done tasks and one cancelled task
- **THEN** the current count is 2, the completed count is 2, and the task list contains all 5

#### Scenario: Reopened task returns to current work
- **WHEN** one of those done tasks is set back to in progress
- **THEN** the current count is 3 and the completed count is 1

### Requirement: Projects participated in
A contact SHALL expose the distinct projects of its contractor tasks (including the company roll-up) and their number, and SHALL let the user open that list.

#### Scenario: Projects from tasks
- **WHEN** "Jane Doe" is contractor of two tasks in project P and one task in project Q
- **THEN** Jane's projects are exactly P and Q, and the project count is 2

### Requirement: History is derived and not editable
Every work-history value SHALL be computed from task records at read time. No user SHALL be able to edit a work-history value, and no separate counter or history record SHALL be kept that could disagree with the tasks.

The next read in the same transaction SHALL reflect changes to tasks, contractor,
state, project, archiving, template status or contact hierarchy without the
caller manually invalidating the cache.

#### Scenario: History follows task changes
- **WHEN** the contractor of a done task is changed from "Jane Doe" to "Dan"
- **THEN** Jane's completed count decreases by one and Dan's increases by one, with no other action

#### Scenario: Read then mutate then read
- **WHEN** a user reads history, reassigns or closes a task, and reads history again in the same transaction without clearing caches
- **THEN** the old and new contractors' lists and counts reflect the committed-in-transaction changes under the viewer's access

### Requirement: History respects the viewer's access
Work-history lists and counts SHALL include only tasks and projects the viewing user is allowed to read. Users without access to Project SHALL NOT see contractor work history on contacts.

#### Scenario: Restricted project hidden from the count
- **WHEN** "Jane Doe" is contractor of a task in a project that user U cannot access, and of a task in a project U can access
- **THEN** U sees one contractor task for Jane

#### Scenario: User without Project access
- **WHEN** an internal user without any Project access opens a contractor contact
- **THEN** no contractor work-history information is shown to them
