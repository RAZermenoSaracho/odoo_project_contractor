## MODIFIED Requirements

### Requirement: Contractor tasks with company roll-up
A contact SHALL expose the tasks for which it is the contractor. For a company, this SHALL also include tasks whose contractor is any contact belonging to that company, following the same parent-contact roll-up Odoo applies to a customer's tasks. Archived tasks and task templates SHALL be excluded.

The task relation returned by a direct read, the history actions and counts SHALL all use these same roll-up and exclusion rules, even when the caller disables the usual archived-record filter.

#### Scenario: Individual contractor tasks
- **WHEN** "Jane Doe" is contractor of tasks T1 and T2
- **THEN** Jane's contractor tasks are exactly T1 and T2

#### Scenario: Company includes its contacts' work
- **WHEN** "Acme Consulting" is contractor of task T3 and its contact "Bob" is contractor of task T4
- **THEN** Acme's contractor tasks are T3 and T4, and Bob's are only T4

#### Scenario: Direct company history and exclusions
- **WHEN** a company and its child contact have ordinary, archived, task-template and project-template assignments and a user reads the company history directly or through navigation
- **THEN** every surface includes the readable ordinary company/child work only, including with archived-record filtering disabled

### Requirement: History is derived and not editable
Every work-history value SHALL be computed from task records at read time. No user SHALL be able to edit a work-history value, and no separate counter or history record SHALL be kept that could disagree with the tasks.

The next read in the same transaction SHALL reflect changes to tasks, contractor, state, project, archiving, template status or contact hierarchy without the caller manually invalidating the cache.

#### Scenario: History follows task changes
- **WHEN** the contractor of a done task is changed from "Jane Doe" to "Dan"
- **THEN** Jane's completed count decreases by one and Dan's increases by one, with no other action

#### Scenario: Read then mutate then read
- **WHEN** a user reads history, reassigns or closes a task, and reads history again in the same transaction without clearing caches
- **THEN** the old and new contractors' lists and counts reflect the committed-in-transaction changes under the viewer's access
