## Report

Implemented the scoped P3 fault-order correction.

- Holds the first exact automatic A retry before `route.fetch`, preserving strict B-behind-A assertions.
- Keeps staged retry identity observable and bounded; different body/key requests remain visible, unexpected duplicates fail closed.
- Added browser-free fault-order/outbox controls.
- Protected Gate5 test, reset/recovery tail, and mounted helper remain byte-identical.

Tests:

- Targeted Node controls: 23 passed.
- Serialized TypeScript checks: all 3 passed.
- Scoped ESLint: passed.
- Playwright list-only: 15 tests discovered.
- `git diff --check`: passed.
- Reverse-removal check: passed.

Hashes:

- Full spec: `26c1ae…` → `b3bc5d…`
- Gate5 test: unchanged `e6cf20…`
- Protected tail: unchanged `acb8d6…`
- Mounted helper: unchanged `164bf2…`

No browser/backend/live journey or full suite was run. Commit message and `DONE` marker were created.