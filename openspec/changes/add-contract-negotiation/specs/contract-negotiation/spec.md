## Purpose

Allows customers to approach contractors and negotiate privately before any authorization to enter a protected contract workspace.

## ADDED Requirements

### Requirement: Customer outreach is private and grants no workspace
An opportunity's customer SHALL be able to approach one or more active published contractors. Each contractor SHALL receive a separate private conversation with only that customer and contractor as participants. The customer SHALL select the brief and documents shared into it; an invitation SHALL NOT disclose protected Project records, workspace documents or other negotiations, add project collaborators/followers, create work grants, or change user type. The caller's customer role SHALL be derived from ownership; selecting a recipient SHALL NOT permit impersonating that recipient.

#### Scenario: Approach two contractors
- **WHEN** a customer approaches contractors A and B about the same opportunity
- **THEN** A sees only their shared brief and conversation, B sees only theirs, and neither receives workspace access or knowledge of the other's offer

#### Scenario: Non-owner invites
- **WHEN** another customer attempts outreach on an opportunity they do not own
- **THEN** the request is denied without disclosing its private content

#### Scenario: Draft opportunity outreach
- **WHEN** the owner contacts a contractor about a draft opportunity
- **THEN** only the explicitly shared conversation snapshot is readable by the recipient and the draft opportunity itself remains owner-only

### Requirement: Participant messages remain in their own channel
Conversation participants SHALL be able to post and read plain or sanitized text messages, with server-derived author and time. Only those participants and authorized marketplace moderators SHALL read them. Internal administrative notes SHALL never appear in the participant stream, including for a restricted internal contractor. Arbitrary recipient lists, follower subscriptions, record relinking and external email routing SHALL NOT widen audiences. Closing a conversation SHALL disable new messages while retaining its participants' history; revoked contractor work access SHALL NOT disclose any new workspace content through history.

#### Scenario: Negotiate before authorization
- **WHEN** a customer and a portal contractor exchange messages before approval or acceptance
- **THEN** both can read that conversation and neither the invitation nor message grants protected work access

#### Scenario: Competing contractor guesses a thread
- **WHEN** contractor B requests A's conversation, messages or attachments by identifier
- **THEN** the workflow returns the same not-found response as for nonexistent identifiers

#### Scenario: Internal contractor reads audit notes
- **WHEN** an approved internal contractor reads their negotiation stream
- **THEN** no administrative notes, tracked private fields or other recipients are returned

### Requirement: Initial price is optional and negotiated offers are versioned
An opportunity SHALL support an optional initial proposed price in its currency and a negotiable flag. No price SHALL mean unspecified, distinct from zero; specified prices SHALL be positive. A fixed initial price SHALL constrain submitted offer amounts, while a negotiable price SHALL permit counteroffers. Messages alone SHALL NOT change a binding offer. Contractors SHALL submit and revise structured offers with price, pricing type, currency and duration; customer counteroffers SHALL be explicit requests that require contractor confirmation into a new offer revision. Previously displayed revisions SHALL remain auditable.

#### Scenario: No initial price
- **WHEN** a customer creates an opportunity without an initial proposed price
- **THEN** contractors can negotiate and submit structured offers without an invented zero-price agreement

#### Scenario: Fixed initial price
- **WHEN** a contractor submits a different amount on an opportunity marked non-negotiable
- **THEN** submission is rejected without modifying the opportunity or agreement

#### Scenario: Customer counteroffer
- **WHEN** a customer suggests a lower price in a conversation
- **THEN** the existing structured offer remains unchanged until its contractor confirms a revised offer

### Requirement: Acceptance checks the exact offer revision
Acceptance SHALL identify the offer revision and terms shown to the customer. If the offer was revised, withdrawn, declined, became ineligible or belongs to another opportunity, acceptance SHALL fail without side effects and request a refresh. When the workspace workflow is installed, acceptance SHALL also carry explicit work authorization and all of its eligibility checks; no legacy acceptance operation SHALL bypass revision or authorization checks.

#### Scenario: Stale browser accepts old terms
- **WHEN** a contractor changes amount from 1000 to 1200 after the customer viewed revision 1 and the customer accepts revision 1
- **THEN** acceptance is rejected and neither assignment nor a grant is created

#### Scenario: Message says accepted
- **WHEN** the customer posts a message saying they accept
- **THEN** no formal acceptance, assignment or workspace access occurs

### Requirement: Negotiation survives losing without execution leakage
One conversation SHALL exist per opportunity and contractor, including concurrent invitations. When the job is filled or cancelled, conversations SHALL become read-only; the winner SHALL use the authorized workspace for execution. Losing contractors SHALL retain only their own conversation snapshot, shared negotiation documents and proposals, never job execution details or workspace resources. Updated snapshots SHALL require an explicit customer share and SHALL NOT mutate frozen accepted terms.

#### Scenario: Another contractor wins
- **WHEN** the customer authorizes A instead of B
- **THEN** B's conversation becomes read-only, its prior shared brief remains available, and all execution details are denied
