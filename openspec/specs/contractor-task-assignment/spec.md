# contractor-task-assignment Specification

## Purpose
Lets a project task record which external contractor performs it, without making the contractor an Odoo user. This stays separate from the task's internal assignees and its customer.

## Requirements

### Requirement: At most one contractor per task
Every task SHALL have an optional contractor: at most one contact who performs the task as an external party. The contractor SHALL be empty by default. A user allowed to edit the task SHALL be able to set, change, or clear it.

#### Scenario: Assign a contractor
- **WHEN** a project user sets "Jane Doe", an eligible contractor, as the contractor of task T
- **THEN** task T's contractor is "Jane Doe"

#### Scenario: Clear a contractor
- **WHEN** the project user clears the contractor of task T
- **THEN** task T has no contractor and its other fields are unchanged

### Requirement: Only eligible contractors can be assigned
Setting or changing a task's contractor SHALL be rejected unless the contact is active, eligible as defined by `contractor-contact-classification`, and belongs to the task's company or to no specific company. A later change to the contact's classification SHALL NOT invalidate contractor values already recorded on tasks.

#### Scenario: Non-contractor rejected
- **WHEN** a project user sets "Carol", who is not eligible, as the contractor of a task
- **THEN** the change is rejected and the task keeps its previous contractor

#### Scenario: Contractor from another company rejected
- **WHEN** a task belongs to company A and a user sets as contractor an eligible contact restricted to company B
- **THEN** the change is rejected

#### Scenario: Existing assignment survives unmarking
- **WHEN** "Jane Doe" is contractor of task T and is later unmarked as a contractor
- **THEN** task T still shows "Jane Doe" as contractor and can be saved with other changes

### Requirement: Contractor is distinct from assignees and customer
A task's contractor SHALL be independent of its internal assignees and its customer. Setting, changing, or clearing the contractor SHALL NOT change the assignees or the customer, and changing those SHALL NOT change the contractor. A contractor SHALL NOT need a user account. A contractor contact that happens to have a user account SHALL NOT be added as an assignee.

#### Scenario: Assignees unchanged
- **WHEN** task T has internal assignees "Alice" and "Ahmed" and a contractor is set
- **THEN** the assignees are still exactly "Alice" and "Ahmed"

#### Scenario: Contractor without user account
- **WHEN** a contact with no user account is set as a task's contractor
- **THEN** the assignment succeeds and no user is created

### Requirement: Several contractors through subtasks
Work performed by several contractors SHALL be represented by subtasks, each with its own contractor. A subtask's contractor SHALL NOT be copied from, or propagated to, its parent task.

#### Scenario: Two contractors on one piece of work
- **WHEN** task T has subtasks T1 with contractor "Jane Doe" and T2 with contractor "Acme Consulting"
- **THEN** T1 and T2 each keep their own contractor and T's contractor is unaffected

### Requirement: Finding contracted work
Task searches SHALL let users filter tasks that have a contractor, filter tasks by a given contractor, and group tasks by contractor. Whether a task is contracted work SHALL be determined only by whether it has a contractor; there SHALL be no separate marker that could disagree with it.

#### Scenario: Filter contracted work
- **WHEN** a project user applies the contracted-work filter in a project's task list
- **THEN** exactly the tasks with a contractor are listed

#### Scenario: Group by contractor
- **WHEN** a project user groups tasks by contractor
- **THEN** tasks appear under their contractor, and tasks without a contractor appear in a group without contractor

### Requirement: Changes are tracked without notifying the contractor
Setting, changing, or clearing a task's contractor SHALL be recorded in the task's change history with the acting user and time. Assigning a contractor SHALL NOT subscribe the contractor to the task and SHALL NOT send the contractor any message.

#### Scenario: Assignment history
- **WHEN** a project user changes task T's contractor from "Jane Doe" to "Acme Consulting"
- **THEN** T's history shows that change and the user who made it
- **AND** neither contact becomes a follower of T or receives an email

### Requirement: Duplicated and template-created tasks start without a contractor
Duplicating a task, creating a task from a task template, or generating a recurring occurrence SHALL produce a task with no contractor.

#### Scenario: Duplicate a contracted task
- **WHEN** a project user duplicates a task whose contractor is "Jane Doe"
- **THEN** the new task has no contractor and the original is unchanged
