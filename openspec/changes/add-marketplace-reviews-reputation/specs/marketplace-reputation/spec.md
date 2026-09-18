## Purpose

Exposes trustworthy contractor statistics that are derived only from legitimate marketplace records: completed jobs and visible reviews. No actor can type a reputation value in or inflate it by hand.

## ADDED Requirements

### Requirement: Derived reputation statistics
Every contractor profile SHALL expose these statistics:
- **completed job count**: the number of jobs assigned to the contractor that are `done`;
- **review count**: the number of reviews of the contractor that are not hidden;
- **average rating**: the arithmetic mean of the ratings of the contractor's non-hidden reviews, rounded to two decimals, or zero when the review count is zero;
- **average completion days**: the mean, over the contractor's `done` jobs, of the elapsed time from assignment to completion in days, rounded to one decimal, or zero when there are no completed jobs.

Readers SHALL treat an average rating of zero with a review count of zero as "no rating yet".

#### Scenario: Statistics from records
- **WHEN** a contractor has three `done` jobs taking 2, 4 and 6 days, one `cancelled` job, and reviews rated 5 and 4 plus one hidden review rated 1
- **THEN** the completed job count is 3, the review count is 2, the average rating is 4.50 and the average completion days is 4.0

#### Scenario: New contractor
- **WHEN** a contractor has no completed jobs and no reviews
- **THEN** all four statistics are zero

### Requirement: Only legitimate records contribute
Cancelled jobs, jobs not yet `done`, hidden reviews, and reviews for jobs not assigned to the contractor SHALL NOT contribute to any statistic.

#### Scenario: Cancelled job excluded
- **WHEN** an `in_progress` job assigned to a contractor is cancelled
- **THEN** the contractor's completed job count and average completion days are unchanged

### Requirement: Statistics stay current
The statistics SHALL reflect the underlying records immediately after any operation that changes them:
- job completion;
- review submission;
- review hiding or unhiding;
- job cancellation.

No scheduled job or manual recalculation SHALL be needed.

#### Scenario: Review updates average
- **WHEN** a contractor with one visible review rated 4 receives a new review rated 2
- **THEN** reading the contractor's profile right after shows review count 2 and average rating 3.00

#### Scenario: Hiding updates average
- **WHEN** a marketplace manager hides that review rated 2
- **THEN** reading the profile right after shows review count 1 and average rating 4.00

### Requirement: Statistics are not manually editable
No actor SHALL be able to set or change any reputation statistic through generic record creation or updates. This includes the contractor, marketplace managers and administrators using ORM or RPC writes.

#### Scenario: Contractor inflates rating
- **WHEN** a contractor sends a generic write setting their average rating to 5
- **THEN** the write is rejected and the average rating is unchanged

#### Scenario: Manager edits completed count
- **WHEN** a marketplace manager sends a generic write setting a profile's completed job count to 50
- **THEN** the write is rejected

### Requirement: Statistics are public with the profile
Reputation statistics SHALL be readable by anyone who can read the profile, including anonymous visitors for published, active profiles.

#### Scenario: Directory shows statistics
- **WHEN** an anonymous visitor reads a published, active profile
- **THEN** its completed job count, review count, average rating and average completion days are returned
