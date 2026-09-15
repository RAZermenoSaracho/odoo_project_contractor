## Purpose

Gives contractors an optional, public-facing marketplace profile, linked one-to-one to their existing contact identity. It holds only information the contractor chooses to publish, and it is the gate that makes a user eligible to submit proposals.

## ADDED Requirements

### Requirement: One profile per contact, linked to the existing identity
The system SHALL allow at most one marketplace profile per contact. A profile SHALL reference an existing contact and SHALL NOT create or duplicate any user or contact identity. Whenever a contractor role is needed, the system SHALL resolve it from the calling user's own contact.

#### Scenario: Second profile for the same contact is rejected
- **WHEN** a user whose contact already has a marketplace profile requests creation of another profile
- **THEN** the request is rejected and no second profile exists for that contact

#### Scenario: No new identity is created
- **WHEN** a portal user creates their marketplace profile
- **THEN** the number of users and contacts is unchanged and the profile references the caller's existing contact

### Requirement: Self-service profile creation for the caller only
Any authenticated user who is not the public user SHALL be able to create a marketplace profile, always for their own contact. The system SHALL derive the profile's contact from the caller and SHALL reject any input that tries to name a different contact. A new profile SHALL start in status `draft` and unpublished.

#### Scenario: Portal user creates own profile
- **WHEN** an authenticated portal user without a profile creates one with a public name and headline
- **THEN** a profile in status `draft`, unpublished, linked to that user's contact is created

#### Scenario: Attempt to create a profile for someone else
- **WHEN** a portal user submits profile creation input that includes another contact's identifier
- **THEN** the request is rejected and no profile is created

#### Scenario: Anonymous visitor cannot create a profile
- **WHEN** an unauthenticated visitor attempts to create a marketplace profile
- **THEN** the request is rejected

### Requirement: Activation classifies the contact as a contractor
When a profile becomes `active`, the system SHALL ensure that its contact is classified as a contractor under the foundation addon's contractor classification. Suspending, unpublishing, or deleting the profile SHALL NOT remove that classification.

#### Scenario: Activation marks the contact
- **WHEN** a contact that is not classified as a contractor activates its complete profile
- **THEN** the contact is classified as a contractor

#### Scenario: Suspension keeps the classification
- **WHEN** a marketplace manager suspends that profile
- **THEN** the contact remains classified as a contractor

### Requirement: Publishable profile content is separate from private contact data
A marketplace profile SHALL contain only these contractor-controlled, publishable fields in v1:
- public name;
- headline;
- biography (plain text);
- skills;
- optional indicative hourly rate and its currency;
- availability (`available`, `limited`, `unavailable`);
- optional country.

Reading a profile SHALL NOT disclose the linked contact's identity or contact data (legal name, email, phone, address, company, or the contact reference itself) to anyone except marketplace managers.

#### Scenario: Directory reader sees only publishable fields
- **WHEN** another portal user or an anonymous visitor reads a published, active profile
- **THEN** they can read the publishable fields and derived reputation statistics
- **AND** they cannot read the linked contact reference or the contact's name, email, phone, or address

#### Scenario: Public name defaults but is independent
- **WHEN** a profile is created without an explicit public name
- **THEN** the public name is initialized from the contact's display name
- **AND** later changes to the contact's name do not change the profile's public name

### Requirement: Profile status lifecycle
A profile SHALL have exactly one status: `draft`, `active`, or `suspended`. The allowed transitions are:
- `draft` → `active`: by the profile owner. It requires a public name, a headline and at least one skill.
- `active` → `suspended`: by a marketplace manager only. It requires a reason.
- `suspended` → `active`: by a marketplace manager only.

No other transition SHALL be possible. When a profile is suspended, the system SHALL close all of that contractor's proposals still in `submitted` with close reason `contractor_suspended`. Jobs already assigned to the contractor SHALL NOT change automatically.

#### Scenario: Owner activates a complete profile
- **WHEN** the owner activates a `draft` profile that has a public name, headline, and at least one skill
- **THEN** the profile becomes `active`

#### Scenario: Incomplete profile cannot be activated
- **WHEN** the owner activates a `draft` profile with no skills
- **THEN** the request is rejected and the profile stays `draft`

#### Scenario: Owner cannot self-reinstate
- **WHEN** the owner of a `suspended` profile attempts to activate it
- **THEN** the request is rejected and the profile stays `suspended`

#### Scenario: Suspension closes pending proposals
- **WHEN** a marketplace manager suspends a profile with a reason while it has two `submitted` proposals and one `accepted` proposal
- **THEN** the two submitted proposals become `closed` with reason `contractor_suspended`
- **AND** the accepted proposal and its job are unchanged

### Requirement: Directory publication
A profile SHALL appear in the contractor directory only while it is both `active` and published. The owner SHALL be able to publish their profile only while it is `active`. The owner or a marketplace manager SHALL be able to unpublish it at any time.

#### Scenario: Publishing a draft profile is rejected
- **WHEN** the owner attempts to publish a `draft` profile
- **THEN** the request is rejected and the profile stays unpublished

#### Scenario: Suspended profile leaves the directory
- **WHEN** a published profile is suspended
- **THEN** anonymous visitors and other portal users can no longer read it, even though its published flag is unchanged

### Requirement: Self-service activation and publication without manager approval
In v1 a profile owner SHALL be able to activate their complete `draft` profile and publish their `active` profile without any manager approval, review, or verification step. Verification SHALL NOT be a precondition for activation, publication, directory listing, or proposal submission. In v1, manager control over profiles SHALL be limited to after-the-fact actions: suspension, reinstatement, unpublishing, and setting or clearing the verification flag. A pre-publication review or approval step is outside v1.

#### Scenario: Owner goes live without a manager
- **WHEN** the owner of a complete `draft` profile activates it and then publishes it, with no manager action at any point
- **THEN** the profile is `active` and published, and anonymous visitors can read it

#### Scenario: Unverified contractor can bid
- **WHEN** the owner of an `active`, unverified profile submits an otherwise eligible proposal
- **THEN** the proposal is created

### Requirement: Verification badge is manager-controlled
A profile SHALL carry a verification flag. Only a marketplace manager SHALL be able to set or clear it; no profile update by the owner SHALL change it.

#### Scenario: Owner cannot self-verify
- **WHEN** a profile owner submits a profile update that includes the verification flag
- **THEN** the request is rejected and the verification flag is unchanged

### Requirement: Owner updates to publishable fields
The profile owner SHALL be able to update the publishable fields while the profile is `draft` or `active`, but not while it is `suspended`. A profile update SHALL NOT change status, publication, verification, the linked contact, or reputation statistics. Any update that includes one of those fields SHALL be rejected as a whole.

#### Scenario: Update headline
- **WHEN** the owner of an `active` profile updates its headline
- **THEN** the headline changes and nothing else does

#### Scenario: Update smuggling a protected field
- **WHEN** the owner submits an update that includes a new headline and a status value
- **THEN** the whole request is rejected and neither field changes

### Requirement: Profile deletion is restricted
Profile owners SHALL NOT delete their profile; they unpublish it instead. A marketplace manager SHALL be able to delete a profile only if no proposal, job, or review references it.

#### Scenario: Referenced profile cannot be deleted
- **WHEN** a marketplace manager attempts to delete a profile that has at least one proposal
- **THEN** the deletion is rejected
