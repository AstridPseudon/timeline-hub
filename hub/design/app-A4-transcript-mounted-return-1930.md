# A4 transcript mounted return 1930

PASS: the existing persistence test now exercises genuine v2 acceptance and refusal semantics through the mounted host → `useTimelineSave` → local save session → durable outbox → generated Runtime client path.

The refusal mock uses the official complete 409 conflict envelope. The test verifies structured conflict classification, visible canonical rollback to `r0/p0`, the user-facing unsaved-association message, and exact retention of the pending serialized body and idempotency key. It no longer treats an unknown/retry response or optimistic association as successful refusal coverage.

The acceptance mock and assertions cover the required accepted v2 data/receipt fields, authoritative step patch/dependency, effective atomic merge mode, canonical closure/digests, exact request base pair/label/steps, omitted reads, raw null/absence and sibling preservation, generated route/key, and receipt `result === data`.

Verification passed: targeted Vitest 4 files/52 tests; app, node, and project TypeScript checks under the shared flock; scoped ESLint; and `git diff --check`. Only the assigned persistence test is changed. No full, browser, live, service, seed, P1, or benchmark suite was run. Legacy config-mirror/collision/shared-row/association-read behavior remains an honest documented gap.
