# Design

Controllers create `{id, name}` values only after the parent Contract, Proposal,
or Project has passed its normal user-context ORM check. Templates consume those
values rather than browsing the protected partner relation. No partner ACL or
record rule changes are required.
