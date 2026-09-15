## Purpose

Lets the customer of a legitimately completed marketplace job leave one rating and review of the contractor who did the work. Reviews cannot be changed after submission; managers can moderate them, but every moderation step is recorded.

## ADDED Requirements

### Requirement: Review eligibility
A review SHALL be submitted only when all of these hold:
- the caller is the job's customer;
- the job is `done`;
- the job has no existing review.

The system SHALL derive the reviewer from the caller and the reviewed contractor from the job's assigned contractor, and SHALL reject input that names either.

#### Scenario: Customer reviews a completed job
- **WHEN** the customer of a `done` job submits a review with rating 5
- **THEN** a review linked to that job and its assigned contractor is created and its submission time is recorded

#### Scenario: Cancelled job
- **WHEN** the customer of a `cancelled` job submits a review
- **THEN** the request is rejected

#### Scenario: Delivered but unconfirmed job
- **WHEN** the customer of a `delivered` job submits a review
- **THEN** the request is rejected

#### Scenario: Contractor reviews themselves
- **WHEN** the assigned contractor submits a review for the job
- **THEN** the request is rejected

#### Scenario: Unrelated user
- **WHEN** a portal user unrelated to a `done` job submits a review for it
- **THEN** the request fails exactly as if the job did not exist

#### Scenario: Contractor spoofing in review input
- **WHEN** the customer submits review input naming a different contractor
- **THEN** the request is rejected

### Requirement: Customer-to-contractor reviews only, with no deadline
In v1 reviews SHALL be written only by a job's customer about that job's assigned contractor. The system SHALL NOT provide any way for a contractor to review a customer. A customer's review eligibility SHALL NOT expire: the time elapsed since the job became `done` SHALL NOT affect it.

#### Scenario: Review long after completion
- **WHEN** the customer of a job that became `done` more than a year ago submits its first review
- **THEN** the review is created

#### Scenario: No review of the customer
- **WHEN** the assigned contractor of a `done` job attempts to submit a review about the job's customer
- **THEN** the request is rejected and no review exists for that job

### Requirement: One review per job
The system SHALL allow at most one review per job, even when submissions arrive concurrently. A hidden review still counts as that job's review.

#### Scenario: Second review
- **WHEN** the customer submits a second review for a `done` job that already has one
- **THEN** the request is rejected

#### Scenario: Concurrent double submission
- **WHEN** two review submissions for the same job arrive at the same time
- **THEN** exactly one review exists afterwards

### Requirement: Review content
A review SHALL contain a whole-number rating from 1 to 5 inclusive, and an optional plain-text comment of at most 2000 characters.

#### Scenario: Out-of-range rating
- **WHEN** the customer submits a review with rating 6
- **THEN** the request is rejected

### Requirement: Reviews are immutable
After submission, no actor, including managers and administrators through generic writes, SHALL be able to change a review's rating, comment, job, reviewer, contractor, or submission time.

#### Scenario: Customer edits rating
- **WHEN** the customer attempts to change their review's rating from 2 to 5
- **THEN** the request is rejected and the rating stays 2

### Requirement: Manager moderation
A marketplace manager SHALL be able to hide a visible review, with a required reason, and unhide a hidden review. A hidden review SHALL NOT be publicly readable and SHALL NOT count toward reputation. Hiding and unhiding SHALL be recorded with manager, time and reason.

Moderation SHALL change only the review's visibility. It SHALL NOT alter, redact, replace, or delete the original rating, comment, or submission time. A hidden review SHALL keep its original content, readable by marketplace managers, the reviewer and the reviewed contractor. Unhiding SHALL restore public visibility of exactly the original content. The system SHALL NOT offer any operation that lets a manager rewrite a review.

#### Scenario: Hide abusive review
- **WHEN** a marketplace manager hides a review with reason "Contains personal data"
- **THEN** anonymous visitors and unrelated portal users can no longer read it, and the contractor's reputation excludes it

#### Scenario: Hide without reason
- **WHEN** a marketplace manager hides a review without a reason
- **THEN** the request is rejected

#### Scenario: Hiding preserves the original review
- **WHEN** a marketplace manager hides a review rated 1 with comment "Terrible work", then later unhides it
- **THEN** while hidden, managers, the reviewer and the contractor still read rating 1 and the original comment
- **AND** after unhiding, the publicly readable rating and comment are exactly the original ones

#### Scenario: Manager cannot rewrite review text
- **WHEN** a marketplace manager attempts to replace an offensive word in a review's comment
- **THEN** the request is rejected and the comment is unchanged; hiding is the only moderation available

### Requirement: Review visibility
A visible review of a contractor whose profile is `active` and published SHALL be readable by anyone, including anonymous visitors. For those readers it SHALL expose only the rating, the comment, the submission time and the reviewed contractor's public profile. It SHALL NOT expose the reviewer's identity or the reviewed job. The reviewer and the reviewed contractor SHALL be able to read their own review, including whether it is hidden. Marketplace managers SHALL be able to read all reviews.

#### Scenario: Public reads a review
- **WHEN** an anonymous visitor reads the reviews of a published, active contractor
- **THEN** each review's rating, comment and submission time are returned, and the reviewer and job are not

#### Scenario: Contractor sees hidden review of self
- **WHEN** a contractor reads a hidden review about themselves
- **THEN** the review is returned with its hidden status
