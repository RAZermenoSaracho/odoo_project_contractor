## Purpose

Provides private contractor applications and administrator-reviewed internal-user approval, independently from marketplace publication and customer rights.

## ADDED Requirements

### Requirement: Applications use the authenticated person's existing identity
An authenticated portal user SHALL be able to create and submit their own contractor application, containing a professional introduction and requested work scope. The application SHALL derive user and contact identity from the caller, reject supplied ownership or approval fields, and never create a duplicate account or contact. Anonymous visitors SHALL first authenticate through normal database signup or invitation policy. At most one pending application SHALL exist per user, including concurrent submissions.

#### Scenario: Portal user applies
- **WHEN** a logged-in portal user submits their application
- **THEN** a pending application references the same user and contact, without changing their account type or work access

#### Scenario: Duplicate submission
- **WHEN** two requests submit an application for the same user concurrently
- **THEN** at most one pending application exists and no duplicate identity is created

#### Scenario: Applicant supplies approval
- **WHEN** an applicant includes an approved state, administrator identity or target user in submitted values
- **THEN** the entire request is rejected

### Requirement: Private review lifecycle
Applications SHALL support draft, pending, approved, rejected, withdrawn and revoked states. Applicants SHALL edit drafts and withdraw pending applications; only settings administrators SHALL approve or reject pending applications and revoke approvals, with a reason for rejection or revocation. A rejected, withdrawn or revoked applicant SHALL be able to submit a new application without erasing prior decisions. Applicants SHALL read their own status and decision reason; unrelated users SHALL neither read nor enumerate applications. Administrative audit notes SHALL remain private.

#### Scenario: Administrator rejects
- **WHEN** a settings administrator rejects a pending application with a reason
- **THEN** the applicant sees the rejection and reason, remains portal, and the decision records the administrator and server time

#### Scenario: Marketplace manager is not an account administrator
- **WHEN** a marketplace manager without settings administration attempts internal approval
- **THEN** approval is denied and no group or grant changes occur

#### Scenario: Same-company colleague
- **WHEN** a colleague under the applicant's commercial entity searches applications
- **THEN** the applicant's application is not returned

### Requirement: Approval is atomic and grants no work
Approval SHALL transition an eligible existing portal user to the verified restricted internal role in one transaction with the application decision. It SHALL preserve user/contact identity, refuse unsupported security configurations or conflicting privileges, and grant no contracts, Project records or other business resources. Repeated approval SHALL NOT repeat provisioning. Accounts already carrying unrelated internal privileges SHALL require explicit separate review and SHALL NOT be silently converted or stripped of employee access.

#### Scenario: Approve a safe portal account
- **WHEN** an administrator approves a pending application on a compatible installation
- **THEN** the same user becomes restricted internal with zero work grants and the application becomes approved

#### Scenario: Isolation verification fails
- **WHEN** approval cannot establish the verified access ceiling
- **THEN** the user stays portal and the application stays pending with no partial group changes

### Requirement: Revocation removes work access and preserves customer identity
Revoking approval SHALL revoke all effective contractor work grants and demote a workflow-managed account to portal atomically, while preserving its contact, application history, customer-owned opportunities and private negotiations. Reapproval SHALL NOT revive old work grants; fresh customer authorization SHALL be required. Existing sessions SHALL obey the new rights on subsequent access.

#### Scenario: Revoke an active contractor
- **WHEN** an administrator revokes an approved contractor with active contracts
- **THEN** protected work becomes inaccessible immediately, the account becomes portal, and their own customer opportunities remain available

#### Scenario: Reapproval does not restore contracts
- **WHEN** the revoked contractor is later approved again
- **THEN** historical contracts remain without effective work grants until explicitly reauthorized by their customer

### Requirement: Publication and customer rights are separate
Customer opportunity creation and upload SHALL require only normal authenticated portal access, not an application, verification badge or contractor approval. Marketplace self-publication SHALL NOT approve internal access. An approved internal account SHALL NOT automatically publish a directory profile. Public profile visibility and administrative application information SHALL remain separate.

#### Scenario: Customer without an application
- **WHEN** a portal user with no contractor application creates an opportunity
- **THEN** creation succeeds under normal customer rules

#### Scenario: Self-published contractor
- **WHEN** a portal contractor activates and publishes their marketplace profile
- **THEN** they remain portal and gain no protected workspace access
