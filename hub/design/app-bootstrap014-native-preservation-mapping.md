## Bootstrap 0.14 preservation mapping

- `createDefaultTimeline.ts`: replace legacy composition publication with the existing durable native create/init adapter.
- `createDefaultTimeline.test.ts`: retain all 12 cases and 61 expectations from pre-rollback `f54cd98e`.
- New-project and lost-response cases preserve exact create identity, H0 guards, command payload, idempotency, and retry equality.
- Headless repair, default selection, alias resolution, CAS metadata merge, additional timeline identity, and opaque headed reuse remain covered.
- `10fa2ff9a` supplies the final95 lock/generated contract; native activation is valid only with that pin.
- Current status: published013 rollback `27912` is immutable historical evidence and its init exclusion does not describe current behavior. Pinned014/native activation is integrated at `1557c312`; original real proof `1021034025-7782` PASS1/exit0 covers create/init, exact lost-ACK retry, reload/restart, raw readback and history2, with the original 2 native tests/61 assertions preserved. Only the bounded `createDefaultTimeline` initializer cut is qualified; `dataProvider.ts:295` and `:1131` remain LIVE under D04/WC10.
