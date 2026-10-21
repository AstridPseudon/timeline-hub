## Bootstrap 0.14 preservation mapping

- `createDefaultTimeline.ts`: replace legacy composition publication with the existing durable native create/init adapter.
- `createDefaultTimeline.test.ts`: retain all 12 cases and 61 expectations from pre-rollback `f54cd98e`.
- New-project and lost-response cases preserve exact create identity, H0 guards, command payload, idempotency, and retry equality.
- Headless repair, default selection, alias resolution, CAS metadata merge, additional timeline identity, and opaque headed reuse remain covered.
- `10fa2ff9a` supplies the final95 lock/generated contract; native activation is valid only with that pin.
- Current published013 rollback coverage remains historical old-release evidence; this source does not claim real Runtime/Agent/Composition qualification.
