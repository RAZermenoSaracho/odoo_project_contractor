## Purpose

Provides reusable portal and backend entry points that let customers and contractors complete the authorized contractor workflow without deployment-specific pages.

## ADDED Requirements

### Requirement: Portal entry and role-aware navigation
The installed workflow SHALL provide authenticated navigation for contractor application/status, own profile, contractor directory, own opportunities, private conversations and active/completed contracts. Customer and contractor roles SHALL coexist on the same account. Signup SHALL honor the database's native registration/invitation policy. Switching a user from portal to restricted internal SHALL preserve access to their permitted frontend pages. Administrators SHALL receive review and moderation navigation; contractors SHALL receive only authorized work navigation.

#### Scenario: New portal applicant
- **WHEN** a visitor follows the contractor application entry
- **THEN** the workflow uses native login/signup or invitation guidance and returns the authenticated user to their own application

#### Scenario: Approved contractor returns to portal
- **WHEN** a user's account is approved as restricted internal and they reopen their conversations page
- **THEN** their own conversations remain available and unrelated backend applications remain inaccessible

### Requirement: Customer can create and upload without contractor verification
Any normal portal customer SHALL be able to create an opportunity, enter its description and optional initial price, upload private documents, browse active published contractors, and approach selected contractors. Forms SHALL clearly distinguish published listing content, explicitly shared negotiation content and private workspace documents. No contractor application or verification SHALL be required of the customer.

#### Scenario: Customer without contractor status
- **WHEN** an authenticated customer with no application or profile creates an opportunity and uploads a draft
- **THEN** both succeed and the draft remains private until explicitly shared

### Requirement: Negotiation and authorization are distinct screens and decisions
Participants SHALL have a private conversation and structured offer UI with visible revision, currency and agreed-term preview. The customer SHALL receive a separate explicit authorize-work confirmation identifying the chosen contractor and terms. The UI SHALL explain any unmet internal-approval prerequisite and SHALL NOT treat sending a message, selecting a contractor, or accepting a stale offer as authorization.

#### Scenario: Contact button
- **WHEN** the customer contacts a directory contractor
- **THEN** the UI opens only their private negotiation and does not show that contract as active work for the contractor

#### Scenario: Confirm work access
- **WHEN** the customer confirms current terms and the explicit work authorization control
- **THEN** the selected contractor receives the authorized contract in active work, with no competitor or unrelated work exposed

### Requirement: Work pages follow effective access
Active/completed contract pages SHALL display only the permitted workspace, terms, task status, participant messages and documents. Available actions SHALL reflect actor and lifecycle permissions; server checks SHALL enforce the same rules if buttons or URLs are forged. Revoked users SHALL receive a neutral inaccessible response and refreshed counts.

#### Scenario: Revoked bookmark
- **WHEN** a contractor opens a previously valid workspace bookmark after revocation
- **THEN** no protected content is returned and active navigation no longer counts that contract

### Requirement: Controllers preserve domain authorization
Every mutation SHALL use an authenticated state-changing request with CSRF protection where applicable, validated allowlisted inputs and domain operations as the requesting user. Controllers SHALL NOT use unrestricted elevated writes or trust actor/ownership identifiers. GET requests SHALL NOT mutate state. Unreadable and nonexistent workflow targets SHALL have equivalent responses; pagination, search, downloads and API calls SHALL use the same authorization. User-authored text SHALL be escaped or sanitized and safely rendered.

#### Scenario: Forged request
- **WHEN** a user forges another customer's opportunity id, an approval field or another contractor's conversation id
- **THEN** the request fails without side effects or private data disclosure

#### Scenario: CSRF and script content
- **WHEN** a state-changing request lacks a valid CSRF token or a message contains executable markup
- **THEN** the request is rejected or the content is rendered inert, respectively, without unauthorized action

### Requirement: Reusable installable workflow delivery
The repository SHALL ship the frontend and required domain/security addons as a documented installable workflow on a compatible Odoo 19 Community database. Installation SHALL not depend on a database name, hostname, proprietary module, hosted tenant, SSO service or organization branding. Standalone foundation installation SHALL remain supported. The complete workflow SHALL include usable loading, empty, validation-error and concurrent-update states, with keyboard-accessible forms and links.

#### Scenario: Clean arbitrary database
- **WHEN** the documented workflow addon is installed on a fresh compatible database with an arbitrary name
- **THEN** native login, customer opportunity/upload, directory/outreach, application/review, negotiation, authorization and active work can all be reached through shipped navigation

#### Scenario: Empty active list
- **WHEN** a contractor has invitations but no authorized work
- **THEN** the active-contract page shows zero active contracts and a helpful empty state without presenting invitations as work
