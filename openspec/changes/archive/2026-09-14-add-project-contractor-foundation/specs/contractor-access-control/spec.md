## Purpose

Keeps contractor information inside Odoo's existing Contacts and Project access model. Being a contractor never grants access, creates accounts, or exposes data to external users.

## ADDED Requirements

### Requirement: Contractor data follows existing access
Reading or changing a task's contractor SHALL require the same access as reading or changing the task. Reading or changing a contact's contractor classification SHALL require the same access as reading or changing the contact. The addon SHALL NOT introduce security groups, access-right entries, or record rules that widen or narrow access to contacts, projects, or tasks.

#### Scenario: Read-only project user
- **WHEN** a user who can read but not edit task T tries to change T's contractor
- **THEN** the change is rejected by the task's existing access rights

#### Scenario: No new security objects
- **WHEN** the addon's security definitions are inspected after installation
- **THEN** no group, access-right entry, or record rule has been added by the addon

### Requirement: Being a contractor grants nothing
Marking a contact as a contractor, or assigning it to a task, SHALL NOT:
- create a user or portal account;
- give any user access to a project or task;
- add the contact as a follower or collaborator;
- send the contact any message.

A contractor contact that already has a portal account SHALL gain no access to a task by being its contractor.

#### Scenario: Portal user assigned as contractor
- **WHEN** a contact that has a portal account is set as contractor of a task in a project not shared with them
- **THEN** that portal user still cannot read the task or the project

### Requirement: Contractor fields are not exposed to portal users
Portal users, including collaborators of shared projects, SHALL NOT be able to read a task's contractor or any contractor work-history value, whether through portal pages, project sharing, or RPC.

#### Scenario: Project-sharing collaborator reads a task
- **WHEN** a portal collaborator of a shared project reads a task whose contractor is "Jane Doe"
- **THEN** the contractor value is not returned to them

#### Scenario: Portal RPC read of the contractor field
- **WHEN** a portal user explicitly requests the contractor field of a task they can otherwise read
- **THEN** the request is refused or returns no contractor value

### Requirement: Multi-company consistency
Contractor assignments and work history SHALL respect the task's company and the user's allowed companies, as the task's customer field does. A user SHALL NOT see contractor work from companies they are not allowed to access.

#### Scenario: Other-company work not counted
- **WHEN** "Jane Doe" is shared across companies, is contractor of a task in company A and of a task in company B, and user U is allowed only company A
- **THEN** U sees one contractor task for Jane
