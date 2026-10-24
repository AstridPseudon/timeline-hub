## P3 review: FAIL

The mounted producer legitimately emits `doc.patch`:

- `timelineLocalSaveHandoff.ts:257–590` captures the verified parent basis and reads.
- `documentPatchIntent.ts:109–223` emits the guarded `clips/id:<clip>/at` patch.
- `localSaveSession.ts:158–188` persists the exact request/outbox metadata.

Findings:

1. `gate5-reset-precondition.ts:58,82` only requires a nonempty readset and equality between top-level and step reads. Mutating both to a wrong clip is accepted. The control mutates only one side, so it tests linkage, not authenticity.

2. `gate5-reset-precondition.ts:161–167` does not bind the settled outbox to expected scope, owner identity, accepted head, receipt, or request key. A settled owner from another project is accepted. `commandOutboxes()` also filters only by timeline ID.

The request observer is correctly armed before the drag, uses exact request/response identity, requires `doc.patch`, captured `before/value`, scope/base, accepted `200`, and preserves the original reset/tail. No tracked edits were made.

Hashes:

- Base: `66354161950d1e747965c095ea97b881d2592708`, tree `9a37265f…`
- Candidate: `bd2356b3b0d489e08ba05a680b2caa97e2d64091`, tree `91b518d9…`
- Spec: `741bcfb9…7d7cd94` → `f3895c34…872894`
- Helper: `52b14c83…af3d9b` → `9b4bf790…16f0d7`
- Control: `456489a9…441a38f` → `3f74f67a…205a5b`
- Required downstream tail hash remains `f7e7abd9233a332adfeea03155d78af05a5d631ffffbecd64691c7014936bb67`.

Checks passed:

- Gate5 control: exit 0
- Playwright list-only: exit 0, 15 tests
- Root/app/node TypeScript checks: exit 0
- Scoped ESLint: exit 0
- `git diff --check`: exit 0

No browser, service, backend, or live-cause inference was performed. The terminal P3 run remains a bounded setup timeout, not evidence of zero POSTs or root cause. Recommended next step: tighten exact readset and owner/basis assertions, then repeat the independent review.