Implemented finite rejection consumer retention in:

- [p1-diagnostic-safety.ts](/home/user/work/wt/ap2-P1-finite-rejection-consumer-2055/tests/e2e/local/p1-diagnostic-safety.ts)
- [p1-diagnostic-safety.test.ts](/home/user/work/wt/ap2-P1-finite-rejection-consumer-2055/tests/e2e/local/p1-diagnostic-safety.test.ts)

Changes:

- Exact 38-code allowlist and classes `TimelineVersionConflictError|Error`.
- Foreign, forged, and untagged values remain `UNKNOWN`.
- Same bounded 32-record ring with deterministic critical-phase retention and honest overflow counts.
- Registered serialized listener test preserves authentic rejection code/class, numeric state, owner alias, and head through 33 later events.
- Original P1/Gate5 bodies unchanged:
  - `4b04ad7e...a72ea8b7f`
  - `2f750118...10a2f7`
  - Gate5 blob `37caf285...e74b1`

Validation passed:

- Targeted Node test: PASS
- Scoped ESLint: PASS
- `tsconfig.app.json`, `tsconfig.node.json`, `tsconfig.json`: PASS
- `git diff --check`: PASS

Finite-list JSON+LF SHA-256: `5f7d9e8f3da6f39c4b4b96a14908b9b9b5f36d33f5940275b6a511fa0ff6b897`

No browser/full suite or producer changes were made. Commit message written and `DONE` marker created.