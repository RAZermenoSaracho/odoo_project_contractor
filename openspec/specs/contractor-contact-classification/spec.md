# contractor-contact-classification Specification

## Purpose
Lets any contact (a person or a company) be marked as an external contractor while remaining an ordinary Odoo contact. It also defines which contacts are eligible to perform contracted project work.

## Requirements

### Requirement: Contractor flag on contacts
Every contact SHALL carry a contractor classification that is off by default. A user allowed to edit a contact SHALL be able to mark or unmark it as a contractor. Marking a contact as a contractor SHALL NOT create a user, a portal account, or any other record representing the contractor's identity: the contractor SHALL remain the same contact.

#### Scenario: Mark an individual as contractor
- **WHEN** a user who can edit contacts marks the individual contact "Jane Doe" as a contractor
- **THEN** "Jane Doe" is a contractor, and the number of users and contacts is unchanged

#### Scenario: Mark a company as contractor
- **WHEN** a user marks the company contact "Acme Consulting" as a contractor
- **THEN** "Acme Consulting" is a contractor

#### Scenario: New contacts are not contractors
- **WHEN** a contact is created without specifying the classification
- **THEN** it is not a contractor

### Requirement: Contractor eligibility includes a contractor company's contacts
A contact SHALL be eligible to perform contracted work when it is marked as a contractor itself, or when its commercial entity (the company it belongs to) is marked as a contractor. Marking or unmarking a company SHALL NOT change the individual classification stored on its contacts.

#### Scenario: Employee of a contractor company
- **WHEN** "Acme Consulting" is a contractor and "Bob" is a contact belonging to "Acme Consulting" with no classification of his own
- **THEN** "Bob" is eligible to perform contracted work

#### Scenario: Contact of a non-contractor company
- **WHEN** "Carol" belongs to "Client Corp", neither "Carol" nor "Client Corp" is marked as a contractor
- **THEN** "Carol" is not eligible

#### Scenario: Individually marked contact under a non-contractor company
- **WHEN** "Dan" belongs to "Client Corp", which is not a contractor, and "Dan" is marked as a contractor
- **THEN** "Dan" is eligible and "Client Corp" is still not a contractor

### Requirement: Finding contractors in Contacts
Contact searches SHALL offer a filter that returns eligible contractors: contacts marked as contractors and contacts whose commercial entity is marked as a contractor.

#### Scenario: Contractor filter
- **WHEN** a user applies the contractor filter in the contact list
- **THEN** exactly the eligible contractors the user can read are listed

### Requirement: Classification is independent from other contact roles
The contractor classification SHALL NOT change or depend on a contact's other roles, such as customer, vendor, or manufacturing subcontractor. A contact MAY be a customer on one project and a contractor on another.

#### Scenario: Customer who is also a contractor
- **WHEN** "Acme Consulting" is the customer of project A and is marked as a contractor
- **THEN** it remains project A's customer and can also be assigned as contractor on tasks of project B

### Requirement: Unmarking and archiving preserve history
Unmarking a contractor or archiving the contact SHALL NOT remove or alter existing contractor assignments on tasks. From then on, the contact SHALL NOT be offered or accepted for new contractor assignments unless it becomes eligible and active again.

#### Scenario: Unmark a contractor with past work
- **WHEN** a contractor with three assigned tasks is unmarked
- **THEN** the three tasks still show that contact as their contractor, and assigning the contact to a fourth task is rejected
